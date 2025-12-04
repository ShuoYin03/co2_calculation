from fastapi import Depends, FastAPI, HTTPException
from spider.co2_spider import CO2Spider
from utils.security import validate_api_key
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright
import logging
from models.form_input import CalculateTaxRequest
from utils.pf_calculate import calc_pf
import asyncio
import random
from config import MAX_CONCURRENT_BROWSERS, BROWSER_ARGS, MIN_REQUEST_DELAY, MAX_REQUEST_DELAY, USE_PROXY, WEBSHARE_API_KEY
from utils.proxy_manager import ProxyManager

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=False,
        args=BROWSER_ARGS,
    )
    spider = CO2Spider()

    proxy_manager = None
    if USE_PROXY and WEBSHARE_API_KEY:
        proxy_manager = ProxyManager(WEBSHARE_API_KEY)
        success = await proxy_manager.fetch_proxies()
        if success and proxy_manager.has_proxies():
            logger.info(f"Proxy enabled with {len(proxy_manager.proxies)} proxies")
        else:
            logger.warning("Proxy enabled but failed to fetch proxies, running without proxy")

    app.state.playwright = playwright
    app.state.browser = browser
    app.state.spider = spider
    app.state.semaphore = asyncio.Semaphore(MAX_CONCURRENT_BROWSERS)
    app.state.proxy_manager = proxy_manager

    yield

    try:
        await browser.close()
        await playwright.stop()
    except Exception as e:
        logger.error(f"Error closing playwright resources: {e}")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
@app.head("/health")
def health_check():
    return {"status": "ok"}

@app.get("/", dependencies=[Depends(validate_api_key)])
def read_root():
    return {"message": "Hello, world!"}

@app.post("/api/calculate-tax", dependencies=[Depends(validate_api_key)])
async def calculate_tax(req: CalculateTaxRequest):
    reg_parts = req.registration.split("/")
    reg_date = f"{reg_parts[1]}-{reg_parts[0]}-01"

    pf = calc_pf(req.power, req.emission)

    async with app.state.semaphore:
        context = None
        page = None
        try:
            # Prepare context options
            context_options = {
                "user_agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/131.0.0.0 Safari/537.36"
                ),
                "viewport": {"width": 1920, "height": 1080},
                "locale": "fr-FR",
                "extra_http_headers": {
                    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
                    "Accept-Language": "fr-FR,fr;q=0.9,en-US;q=0.8,en;q=0.7",
                    "Accept-Encoding": "gzip, deflate, br",
                    "DNT": "1",
                    "Connection": "keep-alive",
                    "Upgrade-Insecure-Requests": "1",
                    "Sec-Fetch-Dest": "document",
                    "Sec-Fetch-Mode": "navigate",
                    "Sec-Fetch-Site": "none",
                    "Sec-Fetch-User": "?1",
                    "Cache-Control": "max-age=0",
                },
            }
            
            # Get fresh proxy for this request
            if app.state.proxy_manager and app.state.proxy_manager.has_proxies():
                proxy = app.state.proxy_manager.get_random_proxy()
                if proxy:
                    context_options["proxy"] = proxy

            context = await app.state.browser.new_context(**context_options)
            
            # 添加随机延迟,避免被网站识别为爬虫
            await asyncio.sleep(random.uniform(MIN_REQUEST_DELAY, MAX_REQUEST_DELAY))

            # 创建新 page (轻量级操作)
            page = await context.new_page()

            tax_amount = await app.state.spider.run(
                page,
                date=reg_date,
                power=str(pf),
                emission=str(req.emission),
                energy=req.energy,
                weight=str(req.weight),
                region=str(req.region),
            )
            tax_amount = float(tax_amount.replace("€", "").replace(",", ".").replace(" ", "").strip())

            return {"result": {
                "tax_amount": tax_amount,
                "total_price": req.price + tax_amount if req.price else None
            }}
        except ValueError as e:
            # known errors from the spider (e.g. navigation/select timeouts)
            logger.error(f"Spider error: {e}")
            raise HTTPException(status_code=502, detail=str(e))
        except Exception as e:
            logger.exception("Unexpected error running spider")
            raise HTTPException(status_code=500, detail="Internal server error")
        finally:
            if page:
                await page.close()
            if context:
                await context.close()
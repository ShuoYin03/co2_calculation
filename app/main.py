from fastapi import Depends, FastAPI, HTTPException
from spider.co2_spider import CO2Spider
from utils.security import validate_api_key
from contextlib import asynccontextmanager
from playwright.async_api import async_playwright
import logging
from models.form_input import CalculateTaxRequest
from utils.pf_calculate import calc_pf

logger = logging.getLogger(__name__)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    playwright = await async_playwright().start()
    browser = await playwright.chromium.launch(
        headless=True,
        args=["--no-sandbox"],
    )
    spider = CO2Spider()

    app.state.playwright = playwright
    app.state.browser = browser
    app.state.spider = spider
    
    yield
    
    try:
        await browser.close()
        await playwright.stop()
    except Exception as e:
        logger.error(f"Error closing playwright resources: {e}")

app = FastAPI(lifespan=lifespan)

@app.get("/", dependencies=[Depends(validate_api_key)])
def read_root():
    return {"message": "Hello, world!"}

@app.post("/api/calculate-tax", dependencies=[Depends(validate_api_key)])
async def calculate_tax(req: CalculateTaxRequest):
    reg_parts = req.registration.split("/")
    reg_date = f"{reg_parts[1]}-{reg_parts[0]}-01"

    pf = calc_pf(req.power, req.emission)
    context = await app.state.browser.new_context(
        user_agent=(
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/114.0.0.0 Safari/537.36"
        ),
        viewport={"width": 1920, "height": 1080},
        locale="fr-FR",
    )
    page = await context.new_page()
    
    try:
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
        await page.close()
from fastapi import Depends, FastAPI
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
        headless=False,
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
    pf = 6
    browser = app.state.browser
    page = await browser.new_page()
    
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

        tax_amount = float(tax_amount.replace("€", "").replace(",", ".").strip())

        return {"result": {
            "tax_amount": tax_amount,
            "total_price": req.price + tax_amount if req.price else None
        }}
    finally:
        await page.close()
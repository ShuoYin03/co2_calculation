from playwright.async_api import Page
from playwright.async_api import TimeoutError, Error
from typing import List, Optional
from spider.selectors import (
    COOKIE_CONSENT_BUTTONS,
    LABEL_AUTONOMIE_50KM_OUI_SELECTORS,
    LABEL_FRANCE_IMPORT_SELECTORS,
    LABEL_INVALIDITE_NON_SELECTORS,
    SELECT_DEMARCHE_SELECTORS,
    SELECT_TYPE_VEHICULE_SELECTORS,
    INPUT_DATE_MISE_EN_CIRCULATION_SELECTORS,
    INPUT_PUISSANCE_ADM_SAISIE_SELECTORS,
    SELECT_ENERGIE_SELECTORS,
    LABEL_RECEPTION_COMMUNAUTAIRE_OUI_SELECTORS,
    INPUT_TAUX_CO2_SAISI_SELECTORS,
    LABEL_VEHICULE_8PLACES_NON_SELECTORS,
    LABEL_PERSON_MORALE_LOCATION_NON_SELECTORS,
    LABEL_PERSONNE_MORALE_NON_SELECTORS,
    INPUT_POIDS_SAISI_SELECTORS,
    SELECT_DEPARTEMENT_SELECTORS,
    BUTTON_RESULT_SELECTORS,
    COUT_CERTIFICAT_SELECTORS
)
import logging
import asyncio
import random

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CO2Spider:
    def __init__(self):
        self.url = "https://www.service-public.fr/simulateur/calcul/cout-certificat-immatriculation"
        
    async def run(self, page: Page, date: str, power: str, emission: str, energy: str, weight: str, region: str):
        await asyncio.sleep(random.uniform(0.2, 0.8))

        max_retries = 3
        for attempt in range(max_retries):
            try:
                await page.goto(self.url, timeout=60000, wait_until="domcontentloaded")
                await self.check_rate_limit(page)
                break  # 成功则跳出循环
            except (TimeoutError, Error) as e:
                if attempt < max_retries - 1:
                    logger.warning(f"Navigation attempt {attempt + 1} failed, retrying after delay...")
                    await asyncio.sleep(random.uniform(2, 5))  # 重试前等待
                    continue

                logger.error(f"Initial navigation error to {self.url} ({e.__class__.__name__}): {e}")

                # 最后一次尝试用更宽松的策略
                try:
                    await asyncio.sleep(3)
                    await page.goto(self.url, timeout=120000, wait_until="networkidle")
                    await self.check_rate_limit(page)
                except TimeoutError as e2:
                    logger.error(f"All navigation attempts failed to {self.url}: {e2}")
                    raise ValueError(f"Navigation to {self.url} failed after {max_retries} retries - possible rate limiting") from e2
        
        await self.handle_cookie_banner(page)
        await self.select(page, SELECT_DEMARCHE_SELECTORS, value="1", error_message="Demarche select not found", timeout=10000)
        await self.click(page, LABEL_FRANCE_IMPORT_SELECTORS, "France import label not found")
        await self.select(page, SELECT_TYPE_VEHICULE_SELECTORS, value="1", error_message="Type vehicule select not found")
        await self.input(page, INPUT_DATE_MISE_EN_CIRCULATION_SELECTORS, content=date, error_message="Date input not found")
        await self.input(page, INPUT_PUISSANCE_ADM_SAISIE_SELECTORS, content=power, error_message="Puissance input not found")
        await self.select(page, SELECT_ENERGIE_SELECTORS, value=energy, error_message="Type vehicule select not found")

        if energy == "3" or energy == "12":
            await self.click(page, LABEL_AUTONOMIE_50KM_OUI_SELECTORS, "autonomie 50km oui label not found")
            
        if energy != "8":
            await self.click(page, LABEL_INVALIDITE_NON_SELECTORS, "Invalidite non label not found", timeout=2000)
            await self.click(page, LABEL_RECEPTION_COMMUNAUTAIRE_OUI_SELECTORS, "Reception communautaire oui label not found")

        if energy != "8":
            await self.input(page, INPUT_TAUX_CO2_SAISI_SELECTORS, content=emission, error_message="Taux CO2 input not found")
            await self.click(page, LABEL_VEHICULE_8PLACES_NON_SELECTORS, "Vehicule 8 places non label not found")
            # if energy != "16" and energy != "1":
            #     await self.click(page, LABEL_PERSON_MORALE_LOCATION_NON_SELECTORS, "Person morale location non label not found")
            #     await self.click(page, LABEL_PERSONNE_MORALE_NON_SELECTORS, "Personne morale non label not found")
            await self.input(page, INPUT_POIDS_SAISI_SELECTORS, content=weight, error_message="Poids input not found")
        await self.select(page, SELECT_DEPARTEMENT_SELECTORS, value=region, error_message="Departement select not found")
        await self.click(page, BUTTON_RESULT_SELECTORS, "Result button not found")

        result = await self.get_text(page, COUT_CERTIFICAT_SELECTORS, error_message="Result text not found")

        return result

    async def check_rate_limit(self, page: Page):
        """Check if the page is showing a rate limit/overload message"""
        try:
            # Check for rate limit message
            # Using a short timeout because if it's there, it should be visible immediately after load
            if await page.get_by_text("Service-public.fr renforce temporairement son dispositif", exact=False).is_visible(timeout=1000):
                logger.error("Rate limit page detected: Service-public.fr renforce temporairement...")
                raise Exception("Rate limit detected: Service-public.fr is overloaded")
            
            if await page.get_by_text("En raison d’un trafic particulièrement important", exact=False).is_visible(timeout=1000):
                logger.error("Rate limit page detected: En raison d’un trafic particulièrement important...")
                raise Exception("Rate limit detected: Service-public.fr is overloaded")
                
        except TimeoutError:
            # Element not found, which is good
            pass

    async def handle_cookie_banner(self, page: Page):
        try:
            for selector in COOKIE_CONSENT_BUTTONS:
                try:
                    # Check if button exists and is visible with a short timeout
                    # We don't want to wait long if it's not there
                    if await page.is_visible(selector, timeout=2000):
                        logger.info(f"Found cookie banner with selector: {selector}")
                        await page.click(selector)
                        await asyncio.sleep(1) # Wait for banner to disappear/animation
                        return
                except:
                    continue
        except Exception as e:
            logger.warning(f"Error handling cookie banner: {e}")

    async def click(
        self,
        page: Page,
        selectors: List[str],
        error_message: str,
        timeout: Optional[int] = 2000
    ):
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, state="visible", timeout=timeout)
                await page.click(selector)
                return
            except TimeoutError:
                await page.locator(selector).count()
            except Exception as e:
                logger.warning(f"Click failed on {selector}: {e}")

        raise ValueError(error_message)

    async def input(
        self,
        page: Page,
        selectors: List[str],
        content: str,
        timeout: int = 1000,
        clear: bool = True,
        error_message: str = None
    ):
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, timeout=timeout)
                if clear:
                    await page.fill(selector, content)
                else:
                    await page.type(selector, content)
                return
            except TimeoutError:
                logger.warning(f"Selector timeout: {selector}")
            except Exception as e:
                logger.warning(f"Input error for selector {selector}: {e}")

        raise ValueError(error_message)

    async def select(
        self,
        page: Page,
        selectors: List[str],
        value: str = None,
        label: str = None,
        index: int = None,
        timeout: int = 1000,
        error_message: Optional[str] = None
    ):
        for select_selector in selectors:
            try:
                await page.wait_for_selector(select_selector, timeout=timeout)
                if value is not None:
                    result = await page.select_option(select_selector, value=value)
                elif label is not None:
                    result = await page.select_option(select_selector, label=label)
                elif index is not None:
                    result = await page.select_option(select_selector, index=index)
                else:
                    raise ValueError("Must provide one of value, label, or index")
                
                if result:
                    return result
                else:
                    logger.warning(f"No options selected for {select_selector} with value '{value}', label '{label}', or index '{index}'")

            except TimeoutError:
                logger.error(f"Selector timeout: {select_selector}")

        raise ValueError(error_message)

    async def get_text(
        self,
        page: Page,
        selectors: List[str],
        timeout: int = 2000,
        error_message: str = "Element not found"
    ) -> str:
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, timeout=timeout)
                el = await page.query_selector(selector)
                if el:
                    text = await el.inner_text()
                    if text.strip():
                        return text.strip()
            except TimeoutError:
                logger.warning(f"Selector timeout: {selector}")
            except Exception as e:
                logger.warning(f"Extract text error for {selector}: {e}")
        raise ValueError(error_message)

    async def close(self):
        await self.browser.close()
        await self.playwright.stop()
from playwright.async_api import Page
from playwright.async_api import TimeoutError
from typing import List, Optional
from spider.selectors import (
    COOKIE_CONSENT_BUTTONS,
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

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CO2Spider:
    def __init__(self):
        self.url = "https://www.service-public.fr/simulateur/calcul/cout-certificat-immatriculation"
        
    async def run(self, page: Page, date: str, power: str, emission: str, energy: str, weight: str, region: str):
        await page.goto(self.url)
        await self.click(page, COOKIE_CONSENT_BUTTONS, "Cookie consent buttons not found")
        await self.select(page, SELECT_DEMARCHE_SELECTORS, value="1", error_message="Demarche select not found")
        await self.click(page, LABEL_FRANCE_IMPORT_SELECTORS, "France import label not found")
        await self.select(page, SELECT_TYPE_VEHICULE_SELECTORS, value="1", error_message="Type vehicule select not found")
        await self.input(page, INPUT_DATE_MISE_EN_CIRCULATION_SELECTORS, content=date, error_message="Date input not found")
        await self.input(page, INPUT_PUISSANCE_ADM_SAISIE_SELECTORS, content=power, error_message="Puissance input not found")
        await self.select(page, SELECT_ENERGIE_SELECTORS, value=energy, error_message="Type vehicule select not found")
        await self.click(page, LABEL_INVALIDITE_NON_SELECTORS, "Invalidite non label not found")
        await self.click(page, LABEL_RECEPTION_COMMUNAUTAIRE_OUI_SELECTORS, "Reception communautaire oui label not found")
        await self.input(page, INPUT_TAUX_CO2_SAISI_SELECTORS, content=emission, error_message="Taux CO2 input not found")
        await self.click(page, LABEL_VEHICULE_8PLACES_NON_SELECTORS, "Vehicule 8 places non label not found")
        await self.click(page, LABEL_PERSON_MORALE_LOCATION_NON_SELECTORS, "Person morale location non label not found")
        await self.click(page, LABEL_PERSONNE_MORALE_NON_SELECTORS, "Personne morale non label not found")
        await self.input(page, INPUT_POIDS_SAISI_SELECTORS, content=weight, error_message="Poids input not found")
        await self.select(page, SELECT_DEPARTEMENT_SELECTORS, value=region, error_message="Departement select not found")
        await self.click(page, BUTTON_RESULT_SELECTORS, "Result button not found")
        result = await self.get_text(page, COUT_CERTIFICAT_SELECTORS, error_message="Result text not found")
        await page.close()

        return result

    async def click(self, 
        page: Page, 
        selectors: List[str],
        error_message: str,
        timeout: Optional[int] = 1000
    ):
        for selector in selectors:
            try:
                await page.wait_for_selector(selector, timeout=timeout)
                await page.click(selector)
                return
            except TimeoutError:
                logger.warning(f"Selector timeout: {selector}")

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

        input()
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

if __name__ == "__main__":
    import asyncio
    spider = CO2Spider()
    asyncio.run(spider.run("2025-07-31", "1000", "100", "1", "1500", "75"))
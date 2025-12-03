import random
import logging
import httpx
from typing import Optional

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, api_key: str):
        self.api_key = api_key
        self.proxies = []
        self.api_url = "https://proxy.webshare.io/api/v2/proxy/list/?mode=direct&page=1&page_size=100"

    async def fetch_proxies(self):
        try:
            headers = {"Authorization": f"Token {self.api_key}"}
            async with httpx.AsyncClient() as client:
                response = await client.get(self.api_url, headers=headers, timeout=10.0)
                response.raise_for_status()
                data = response.json()

                self.proxies = []
                for proxy in data.get("results", []):
                    proxy_url = f"http://{proxy['username']}:{proxy['password']}@{proxy['proxy_address']}:{proxy['port']}"
                    self.proxies.append(proxy_url)

                logger.info(f"Fetched {len(self.proxies)} proxies from Webshare API")
                return True
        except Exception as e:
            logger.error(f"Error fetching proxies from Webshare: {e}")
            return False

    def get_random_proxy(self) -> Optional[dict]:
        if not self.proxies:
            return None

        proxy_url = random.choice(self.proxies)
        return {"server": proxy_url}

    def has_proxies(self) -> bool:
        return len(self.proxies) > 0

import os
from dotenv import load_dotenv

load_dotenv()

MAX_CONCURRENT_BROWSERS = int(os.getenv("MAX_CONCURRENT_BROWSERS", "2"))

MIN_REQUEST_DELAY = float(os.getenv("MIN_REQUEST_DELAY", "0.5"))
MAX_REQUEST_DELAY = float(os.getenv("MAX_REQUEST_DELAY", "2.0"))

WORKERS = int(os.getenv("WORKERS", "1"))

BROWSER_ARGS = [
    "--no-sandbox",
    "--disable-setuid-sandbox",
    "--disable-dev-shm-usage",
    "--disable-gpu"
]

NAVIGATION_TIMEOUT = int(os.getenv("NAVIGATION_TIMEOUT", "60000"))
NAVIGATION_RETRY_TIMEOUT = int(os.getenv("NAVIGATION_RETRY_TIMEOUT", "120000"))
SELECTOR_TIMEOUT = int(os.getenv("SELECTOR_TIMEOUT", "2000"))

HOST = os.getenv("HOST", "0.0.0.0")
PORT = int(os.getenv("PORT", "8000"))

LOG_LEVEL = os.getenv("LOG_LEVEL", "info")

WEBSHARE_API_KEY = os.getenv("WEBSHARE_API_KEY", "")
USE_PROXY = os.getenv("USE_PROXY", "false").lower() == "true"
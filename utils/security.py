import os
import dotenv
import secrets
from fastapi import Security, HTTPException
from fastapi.security import APIKeyHeader

dotenv.load_dotenv()
API_KEY = os.getenv("API_KEY")
api_key_header = APIKeyHeader(name="x-api-key", auto_error=False)

def validate_api_key(key: str = Security(api_key_header)) -> str:
    if not key or not secrets.compare_digest(key, API_KEY or ""):
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")
    return key

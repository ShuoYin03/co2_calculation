from fastapi import Depends, FastAPI
from utils.security import validate_api_key

app = FastAPI()

@app.get("/", dependencies=[Depends(validate_api_key)])
def read_root():
    return {"message": "Hello, world!"}
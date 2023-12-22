from fastapi import FastAPI
from routes.recognition import router as recognition_router

app = FastAPI()

app.include_router(recognition_router.router)

@app.get("/")
async def index():
    return {"message": "home"}

@app.get("/test")
async def test():
    return {"message": "test"}
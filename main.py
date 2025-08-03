from fastapi import FastAPI
from routers import ping

app = FastAPI(title="Kraftor.ai Backend")

app.include_router(ping.router)

@app.get("/")
def root():
    return {"message": "Welcome to Kraftor.ai Backend"}
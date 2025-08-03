from fastapi import FastAPI
from routers import ping
from routes import transformer  # ✅ New import

app = FastAPI(title="Kraftor.ai Backend")

app.include_router(ping.router)
app.include_router(transformer.router)  # ✅ Register new router

@app.get("/")
def root():
    return {"message": "Welcome to Kraftor.ai Backend"}

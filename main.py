# --- Main FastAPI Application ---

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, BackgroundTasks, HTTPException, Depends
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Local imports from your project structure
from models import (
    RepurposedContent, BrandProfile, Plugin,
    PublishNowRequest, ProcessSourceRequest, ElevenLabsProxyRequest
)
from utils.database import JSONDatabase
from utils.security import encrypt, decrypt
from services.scheduler import create_scheduler
from services.tasks import run_content_processing_task
from services.publishing import publish_content_logic # Moved logic to a service
from routers import content, management, proxy # Import routers

# --- Application Setup ---

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Create a dictionary to hold application state, like the scheduler and db
app_state = {}

# Lifespan manager for startup and shutdown events
@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Handles application startup and shutdown logic.
    """
    # Initialize and load the database
    db = JSONDatabase('db.json')
    db.load()
    app_state["db"] = db
    logger.info("Database loaded successfully.")

    # Create and start the cron job scheduler
    scheduler = create_scheduler(db=db, encrypt_func=encrypt, decrypt_func=decrypt)
    scheduler.start()
    app_state["scheduler"] = scheduler
    logger.info("APScheduler started with cron jobs.")

    yield  # The application is now running

    # Shutdown the scheduler
    app_state["scheduler"].shutdown()
    logger.info("APScheduler shut down gracefully.")

# Initialize the FastAPI app with the lifespan manager
app = FastAPI(
    lifespan=lifespan,
    title="Kraftor.ai Backend API",
    description="A robust backend for the Kraftor.ai platform using FastAPI.",
    version="1.0.0"
)

# --- Dependency Injection ---
# This makes it easy for routers to get access to the database
def get_db() -> JSONDatabase:
    return app_state["db"]

# --- Include Routers ---
# This keeps your main.py file clean and organizes endpoints logically
app.include_router(content.router)
app.include_router(management.router)
app.include_router(proxy.router)

# --- Health Check Endpoint ---
@app.get("/health")
def health_check():
    """A simple endpoint to confirm the API is running."""
    return {"status": "ok"}

# To run: uvicorn main:app --reload

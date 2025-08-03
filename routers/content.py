# --- Router for Content-Related Endpoints ---

from fastapi import APIRouter, Depends, BackgroundTasks, HTTPException
from ..models import PublishNowRequest, ProcessSourceRequest
from ..utils.database import JSONDatabase
from ..services.publishing import publish_content_logic
from ..services.tasks import run_content_processing_task
from ..utils.security import decrypt
from ..main import get_db # Import dependency from main
import logging

router = APIRouter(
    prefix="/content",
    tags=["Content"],
)
logger = logging.getLogger(__name__)

@router.post("/publish_now", status_code=200)
async def publish_now_endpoint(
    request: PublishNowRequest,
    db: JSONDatabase = Depends(get_db)
):
    """
    Manually triggers a single piece of content to be published immediately.
    """
    logger.info(f"Received manual publish request for content_id: {request.content_id}")
    success, message = await publish_content_logic(request.content_id, db, decrypt)
    if not success:
        raise HTTPException(status_code=500, detail=message)
    return {"status": "success", "message": message}

@router.post("/process_source", status_code=202)
async def process_source_content_endpoint(
    request: ProcessSourceRequest,
    background_tasks: BackgroundTasks,
    db: JSONDatabase = Depends(get_db)
):
    """
    Accepts a source URL for background processing (transcription/scraping).
    """
    logger.info(f"Received request to process source content: {request.source_url}")
    background_tasks.add_task(
        run_content_processing_task,
        request.content_id,
        request.source_url,
        request.content_type,
        db
    )
    return {"status": "processing", "message": "Content processing has started in the background."}

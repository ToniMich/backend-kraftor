# --- Router for Securely Proxying External APIs ---

from fastapi import APIRouter, Depends, HTTPException
from ..models import ElevenLabsProxyRequest
from ..utils.database import JSONDatabase
from ..utils.security import decrypt
from ..main import get_db
import logging

router = APIRouter(
    prefix="/proxy",
    tags=["Proxy"],
)
logger = logging.getLogger(__name__)

@router.post("/elevenlabs_tts")
async def elevenlabs_tts_proxy_endpoint(
    request: ElevenLabsProxyRequest,
    db: JSONDatabase = Depends(get_db)
):
    """
    Securely proxies text-to-speech requests to the ElevenLabs API.
    """
    logger.info(f"Proxying request to ElevenLabs for user_id: {request.user_id}")
    plugin = db.get('plugins', request.user_id)
    if not plugin or 'elevenlabs_api_key_encrypted' not in plugin:
        raise HTTPException(status_code=404, detail="API key for this user not found.")

    try:
        api_key = decrypt(plugin['elevenlabs_api_key_encrypted'])
    except Exception:
        raise HTTPException(status_code=500, detail="Failed to decrypt API key.")

    logger.info(f"Simulating ElevenLabs API call for voice_id: {request.voice_id}")
    return {"status": "success", "message": "Simulated audio generation request sent successfully."}

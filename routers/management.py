# --- Router for Data Management Endpoints (Brands, Plugins, etc.) ---

from fastapi import APIRouter, Depends, HTTPException
from ..models import BrandProfile, Plugin, RepurposedContent
from ..utils.database import JSONDatabase
from ..utils.security import encrypt
from ..main import get_db
import logging

router = APIRouter(
    prefix="/manage",
    tags=["Management"],
)
logger = logging.getLogger(__name__)

@router.post("/brands", status_code=201, response_model=BrandProfile)
def create_brand_profile(brand: BrandProfile, db: JSONDatabase = Depends(get_db)):
    """Creates a new brand profile."""
    if db.get('brand_profiles', brand.brand_id):
        raise HTTPException(status_code=409, detail="Brand profile with this ID already exists.")
    
    # Encrypt sensitive tokens before saving
    for account in brand.platform_accounts.values():
        if account.access_token:
            account.access_token = encrypt(account.access_token)
        if account.refresh_token:
            account.refresh_token = encrypt(account.refresh_token)

    db.set('brand_profiles', brand.brand_id,

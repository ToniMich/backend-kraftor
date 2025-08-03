# --- Core Publishing Service Logic ---

import logging
from ..models import RepurposedContent
from ..utils.database import JSONDatabase
from .tasks import mock_publish_to_platform # Assuming mocks are in tasks for now
from datetime import datetime

logger = logging.getLogger(__name__)

async def publish_content_logic(content_id: str, db: JSONDatabase, decrypt_func) -> (bool, str):
    """Core logic for publishing content, usable by manual and auto triggers."""
    post_data = db.get('repurposed_content', content_id)
    if not post_data:
        return False, "Content not found."

    post = RepurposedContent(**post_data)
    
    # Find the associated brand profile
    brand_profile = None
    for profile in db.get_all('brand_profiles'):
        if post.original_content_id in profile.get('original_content', {}):
            brand_profile = profile
            break
    
    if not brand_profile:
        post.publishing_error = "Brand profile not found."
        db.set('repurposed_content', content_id, post.dict())
        return False, post.publishing_error

    platform_account = brand_profile.get('platform_accounts', {}).get(post.platform)
    if not platform_account or not platform_account.get('is_connected'):
        post.publishing_error = f"Platform '{post.platform}' not connected."
        db.set('repurposed_content', content_id, post.dict())
        return False, post.publishing_error
    
    try:
        access_token = decrypt_func(platform_account['access_token'])
    except Exception:
        return False, "Failed to decrypt access token."

    success, message = mock_publish_to_platform(post.platform, post.generated_text, post.media_url, access_token)

    if success:
        post.status = "published"
        post.published_date = datetime.utcnow()
        post.publishing_error = None
        logger.info(f"Successfully published content {content_id} to {post.platform}.")
    else:
        post.status = "failed"
        post.publishing_error = message
        logger.error(f"Failed to publish content {content_id}: {message}")

    db.set('repurposed_content', content_id, post.dict())
    return success, message

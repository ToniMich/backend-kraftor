from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field


class PlatformAccount(BaseModel):
    is_connected: bool
    access_token: Optional[str] = None
    refresh_token: Optional[str] = None


class RepurposedContent(BaseModel):
    content_id: str
    original_content_id: str
    platform: str
    generated_text: str
    media_url: Optional[str] = None
    status: str = Field(default="pending")
    published_date: Optional[datetime] = None
    publishing_error: Optional[str] = None


class BrandProfile(BaseModel):
    brand_id: str
    brand_name: str
    platform_accounts: Dict[str, PlatformAccount]
    original_content: Dict[str, Any] = Field(default_factory=dict)


class Plugin(BaseModel):
    user_id: str
    elevenlabs_api_key: Optional[str] = None


class PublishNowRequest(BaseModel):
    content_id: str


class ProcessSourceRequest(BaseModel):
    content_id: str
    source_url: str
    content_type: str


class ElevenLabsProxyRequest(BaseModel):
    user_id: str
    voice_id: str
    text: str



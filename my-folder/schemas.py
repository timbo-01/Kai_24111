from datetime import datetime
from pydantic import BaseModel, HttpUrl, field_validator
import validators


class URLCreate(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL не может быть пустым")
        if len(v) > 2048:
            raise ValueError("URL слишком длинный (макс. 2048 символов)")
        # validators.url умеет проверять http/https/ftp и т.п.
        if not validators.url(v):
            raise ValueError("Некорректный URL")
        return v


class LinkInfo(BaseModel):
    short_code: str
    original_url: str
    short_url: str
    created_at: datetime
    clicks: int

    class Config:
        from_attributes = True
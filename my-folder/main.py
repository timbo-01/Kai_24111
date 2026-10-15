from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from pydantic import BaseModel, field_validator
import validators

from database import Base, engine, get_db
import crud

Base.metadata.create_all(bind=engine)

app = FastAPI(title="URL Shortener")
templates = Jinja2Templates(directory="templates")

BASE_URL = "http://localhost:8000"


class URLCreate(BaseModel):
    url: str

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("URL не может быть пустым")
        if len(v) > 2048:
            raise ValueError("URL слишком длинный")
        if not validators.url(v):
            raise ValueError("Некорректный URL")
        return v


class LinkInfo(BaseModel):
    short_code: str
    original_url: str
    short_url: str


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    # ⬇️ новый синтаксис Starlette
    return templates.TemplateResponse(request=request, name="index.html")


@app.post("/shorten", response_model=LinkInfo, status_code=201)
def shorten_url(payload: URLCreate, db: Session = Depends(get_db)):
    link = crud.create_short_link(db, payload.url)
    return LinkInfo(
        short_code=link.short_code,
        original_url=link.original_url,
        short_url=f"{BASE_URL}/{link.short_code}",
    )


@app.get("/{code}")
def redirect(code: str, db: Session = Depends(get_db)):
    link = crud.get_link_by_code(db, code)
    if not link:
        raise HTTPException(status_code=404, detail="Ссылка не найдена")
    crud.increment_clicks(db, link)
    return RedirectResponse(url=link.original_url, status_code=302)
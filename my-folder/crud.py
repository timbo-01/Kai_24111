import secrets
import string
from sqlalchemy.orm import Session
from models import Link

ALPHABET = string.ascii_letters + string.digits
CODE_LENGTH = 6


def _generate_code(db: Session) -> str:
    """Генерирует уникальный код заданной длины."""
    for _ in range(10):
        code = "".join(secrets.choice(ALPHABET) for _ in range(CODE_LENGTH))
        if not db.query(Link).filter(Link.short_code == code).first():
            return code
    raise RuntimeError("Не удалось сгенерировать уникальный код")


def create_short_link(db: Session, original_url: str) -> Link:
    existing = db.query(Link).filter(Link.original_url == original_url).first()
    if existing:
        return existing

    link = Link(short_code=_generate_code(db), original_url=original_url)
    db.add(link)
    db.commit()
    db.refresh(link)
    return link


def get_link_by_code(db: Session, code: str) -> Link | None:
    return db.query(Link).filter(Link.short_code == code).first()


def increment_clicks(db: Session, link: Link) -> None:
    link.clicks += 1
    db.commit()
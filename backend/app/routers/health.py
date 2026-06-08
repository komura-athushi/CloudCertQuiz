from fastapi import APIRouter, Depends

from app.db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text

router = APIRouter(
    prefix="/health",   # このファイルのAPIは/healthから始まる
    tags=["health"],   # Swagger UI上での分離する名前
)

@router.get("/")
def health_check():
    return {"status": "ok"}

@router.get("/db")
def db_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT question_text FROM questions LIMIT 1")).scalar()
    return {
        "db": "ok",
        "result": result,
    }

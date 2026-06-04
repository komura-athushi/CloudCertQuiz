from fastapi import APIRouter, Depends
from db.session import get_db
from sqlalchemy.orm import Session
from sqlalchemy import text


router = APIRouter(
    prefix="/questions",   # このファイルのAPIは/questionsから始まる
    tags=["questions"],   # Swagger UI上での分離する名前
)

@router.get("/db-health")
def db_health_check(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT question_text FROM questions LIMIT 1")).scalar()
    return {
        "db": "ok",
        "result": result,
    }

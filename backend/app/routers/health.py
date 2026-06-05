from fastapi import APIRouter

router = APIRouter(
    prefix="/health",   # このファイルのAPIは/healthから始まる
    tags=["health"],   # Swagger UI上での分離する名前
)

@router.get("/")
def health_check():
    return {"status": "ok"}

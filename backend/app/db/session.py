from pathlib import Path
import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.engine import URL

# .env を明示的に読み込む
load_dotenv(Path(__file__).resolve().parents[1] / ".env")


DATABASE_URL = URL.create(
    drivername="mysql+pymysql",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    database=os.getenv("DB_NAME"),
    query={"charset": "utf8mb4"},
)


engine = create_engine(
    DATABASE_URL,
    echo=True,          # SQLログを出す。開発中だけTrueでよい
    pool_pre_ping=True, # 切れた接続を事前検知しやすくする
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

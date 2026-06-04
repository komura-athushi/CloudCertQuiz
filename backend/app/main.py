from fastapi import FastAPI

from routers import health, questions


app = FastAPI()
app.include_router(health.router)  # health.pyのルーターを登録
app.include_router(questions.router)  # questions.pyのルーターを登録

@app.get("/")
def read_root():
    return {"Hello": "World"}

from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.exams import Exam

class ExamRepository:
    def __init__(self, db: Session) -> None:
        
        self.db = db
        
    # IDでexamを検索するメソッド
    def find_by_id(self, exam_id: int) -> Exam | None:
        stmt = (
            select(Exam)
            .where(Exam.id == exam_id)
        )
        return self.db.execute(stmt).scalar_one_or_none()

    def find_all(self) -> list[Exam]:
        stmt = select(Exam)
        return self.db.execute(stmt).scalars().all()

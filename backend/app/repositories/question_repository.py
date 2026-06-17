from sqlalchemy import select
from sqlalchemy.orm import Session, selectinload

from app.models.question import Question


class QuestionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def find_all_by_exam_id(self, exam_id: int) -> list[Question]:
        stmt = (
            select(Question)
            .options(selectinload(Question.choices))
            .where(Question.exam_id == exam_id)
        )
        return self.db.execute(stmt).scalars().all()

    # IDでquestionを検索するメソッド
    def find_by_id(self, question_id: int) -> Question | None:
        stmt = (
            select(Question)
            .options(selectinload(Question.choices))    # choicesも一緒にロードする
            .where(Question.id == question_id)
        )
        
        # SQL文を実行
        return self.db.execute(stmt).scalar_one_or_none()

    def find_by_exam_id_and_id(self, exam_id: int, question_id: int) -> Question | None:
        stmt = (
            select(Question)
            .options(selectinload(Question.choices))
            .where(
                Question.exam_id == exam_id,
                Question.id == question_id,
            )
        )
        return self.db.execute(stmt).scalar_one_or_none()

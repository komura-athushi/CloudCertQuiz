from app.models.exams import Exam
from app.repositories.exam_repository import ExamRepository

class GetExamUseCase:
    def __init__(self, exam_repository: ExamRepository) -> None:
        self.exam_repository = exam_repository

    def execute(self, exam_id: int) -> Exam | None:
        return self.exam_repository.find_by_id(exam_id)

    def execute_all(self) -> list[Exam]:
        return self.exam_repository.find_all()

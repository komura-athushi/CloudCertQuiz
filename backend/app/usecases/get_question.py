from app.models.question import Question
from app.repositories.question_repository import QuestionRepository

# Repositoryを受け取って、質問を取得するユースケース
# 色々なユースケースに合わせたロジックをここに書いていく
class GetQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository) -> None:
        self.question_repository = question_repository

    def execute_all_by_exam_id(self, exam_id: int) -> list[Question]:
        return self.question_repository.find_all_by_exam_id(exam_id)

    def execute(self, question_id: int) -> Question | None:
        return self.question_repository.find_by_id(question_id)

    def execute_by_exam_id(self, exam_id: int, question_id: int) -> Question | None:
        return self.question_repository.find_by_exam_id_and_id(
            exam_id=exam_id,
            question_id=question_id,
        )

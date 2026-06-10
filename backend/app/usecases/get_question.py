from app.models.question import Question
from app.repositories.question_repository import QuestionRepository

# Repositoryを受け取って、質問を取得するユースケース
# 色々なユースケースに合わせたロジックをここに書いていく
class GetQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository) -> None:
        self.question_repository = question_repository

    def execute(self, question_id: int) -> Question | None:
        return self.question_repository.find_by_id(question_id)

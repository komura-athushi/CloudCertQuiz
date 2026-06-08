from app.models.question import Question
from app.repositories.question_repository import QuestionRepository

# Repositoryを受け取って、質問を取得するユースケース
# 色々なユースケースに合わせたロジックをここに書いていく
class GetQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository) -> None:
        self.question_repository = question_repository

    def execute(self, question_id: int) -> Question | None:
        return self.question_repository.find_by_id(question_id)

    # Questions.idとchoices.idを受け取って、正解かどうかを判定するユースケース
    def check_answer(self, question_id: int, choice_id: int) -> bool:
        question = self.question_repository.find_by_id(question_id)

        if question is None:
            raise ValueError("Question not found")

        for choice in question.choices:
            if choice.id == choice_id:
                return True

        return False

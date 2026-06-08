from dataclasses import dataclass

from app.models.question import Question, Choice
from app.repositories.question_repository import QuestionRepository


@dataclass
class AnswerQuestionResult:
    question_id: int
    selected_choice_id: int
    is_correct: bool
    question: Question    

class AnswerQuestionUseCase:
    def __init__(self, question_repository: QuestionRepository) -> None:
        self.question_repository = question_repository

    def execute(self, question_id: int, selected_choice_id: int) -> AnswerQuestionResult:
        question = self.question_repository.find_by_id(question_id)

        if question is None:
            raise ValueError("Question not found")

        selected_choice = None
        
        for choice in question.choices:
            if choice.id == selected_choice_id:
                selected_choice = choice
        
        if selected_choice is None:
            raise ValueError("Selected choice does not belong to this question")
        
        return AnswerQuestionResult(
            question_id=question.id,
            selected_choice_id=selected_choice.id,
            is_correct=selected_choice.is_correct,
            question=question
        )

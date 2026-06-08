from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import QuestionResponse, AnswerResponse, ChoiceResponse, ChoiceAnswerResponse, QuestionAnswerResponse
from app.usecases.get_question import GetQuestionUseCase
from app.usecases.answer_question import AnswerQuestionUseCase, AnswerQuestionResult


router = APIRouter(
    prefix="/questions",    # このファイルのAPIは/questionsから始まる
    tags=["questions"],
)


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionResponse:
    repository = QuestionRepository(db)
    usecase = GetQuestionUseCase(repository)

    question = usecase.execute(question_id)

    if question is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    return QuestionResponse(
        id=question.id,
        question_text=question.question_text,
        choices=question.choices,
    )

@router.post("/{question_id}/answer", response_model=AnswerResponse)
def answer_question(
    question_id: int,
    selected_choice_id: int,
    db: Session = Depends(get_db),
) -> AnswerResponse:
    repository = QuestionRepository(db)
    usecase = AnswerQuestionUseCase(repository)

    try:
        result = usecase.execute(
            question_id=question_id,
            selected_choice_id=selected_choice_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error),
        )

    if result is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Question not found",
        )

    return AnswerResponse(
        question_id=result.question_id,
        selected_choice_id=result.selected_choice_id,
        is_correct=result.is_correct,
        question=QuestionAnswerResponse(
            id=result.question.id,
            question_text=result.question.question_text,
            explanation=result.question.explanation,
            choices=[
                ChoiceAnswerResponse(
                    id=choice.id,
                    choice_text=choice.choice_text,
                    is_correct=choice.is_correct
                )
                for choice in result.question.choices
            ]
        )
    )

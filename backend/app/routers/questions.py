from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.repositories.question_repository import QuestionRepository
from app.schemas.question import AnswerRequest, AnswerResponse, ChoiceAnswerResponse, QuestionAnswerResponse, QuestionResponse
from app.usecases.get_question import GetQuestionUseCase
from app.usecases.answer_question import AnswerQuestionUseCase


router = APIRouter(
    prefix="/exams/{exam_id}/questions",
    tags=["questions"],
)


@router.get("", response_model=list[QuestionResponse])
def get_questions(
    exam_id: int,
    db: Session = Depends(get_db),
) -> list[QuestionResponse]:
    repository = QuestionRepository(db)
    usecase = GetQuestionUseCase(repository)

    questions = usecase.execute_all_by_exam_id(exam_id)

    return [
        QuestionResponse(
            id=question.id,
            question_text=question.question_text,
            choices=question.choices,
        )
        for question in questions
    ]


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    exam_id: int,
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionResponse:
    repository = QuestionRepository(db)
    usecase = GetQuestionUseCase(repository)

    question = usecase.execute_by_exam_id(
        exam_id=exam_id,
        question_id=question_id,
    )

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
    exam_id: int,
    question_id: int,
    request: AnswerRequest,     # JSONのリクエストボディをAnswerRequestモデルとして受け取る
    db: Session = Depends(get_db),
) -> AnswerResponse:
    repository = QuestionRepository(db)
    usecase = AnswerQuestionUseCase(repository)

    try:
        result = usecase.execute(
            exam_id=exam_id,
            question_id=question_id,
            selected_choice_id=request.selected_choice_id,
        )
    except ValueError as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
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

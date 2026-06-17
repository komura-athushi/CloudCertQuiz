from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.db.session import get_db
from app.repositories.exam_repository import ExamRepository
from app.schemas.exam import ExamResponse
from app.usecases.get_exam import GetExamUseCase


router = APIRouter(
    prefix="/exams",    # このファイルのAPIは/examsから始まる
    tags=["exams"],
)

@router.get("/", response_model=list[ExamResponse])
def get_exams(
    db: Session = Depends(get_db),
) -> list[ExamResponse]:
    repository = ExamRepository(db)
    usecase = GetExamUseCase(repository)

    exams = usecase.execute_all()
    return [ExamResponse(
        id=exam.id,
        name=exam.name,
        description=exam.description,
    ) for exam in exams]

@router.get("/{exam_id}", response_model=ExamResponse)
def get_exam(
    exam_id: int,
    db: Session = Depends(get_db),
) -> ExamResponse:
    repository = ExamRepository(db)
    usecase = GetExamUseCase(repository)

    exam = usecase.execute(exam_id)

    if exam is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )

    return ExamResponse(
        id=exam.id,
        name=exam.name,
        description=exam.description,
    )

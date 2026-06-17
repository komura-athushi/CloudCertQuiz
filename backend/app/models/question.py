from __future__ import annotations

from sqlalchemy import Boolean, ForeignKey, Index, Text, text
from sqlalchemy.dialects import mysql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.mixins import TimestampMixin


# Question モデル
class Question(TimestampMixin, Base):
    __tablename__ = "questions"

    __table_args__ = {
        "mysql_engine": "InnoDB",
        "mysql_charset": "utf8mb4",
        "mysql_collate": "utf8mb4_0900_ai_ci",
    }

    id: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )
    
    exam_id: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        ForeignKey("exams.id", ondelete="CASCADE"),
        nullable=False,
    )

    # 問題文
    question_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    # 解説
    explanation: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    # 問題の選択肢
    choices: Mapped[list["Choice"]] = relationship(
        back_populates="question",
        cascade="all, delete-orphan",
    )
    
    exam: Mapped[Exam] = relationship(
        back_populates="questions",
    )
    

# 選択肢モデル
class Choice(TimestampMixin, Base):
    __tablename__ = "choices"

    __table_args__ = (
        Index("ix_choices_question_id", "question_id"),
        {
            "mysql_engine": "InnoDB",
            "mysql_charset": "utf8mb4",
            "mysql_collate": "utf8mb4_0900_ai_ci",
        },
    )

    id: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        primary_key=True,
        autoincrement=True,
    )

    question_id: Mapped[int] = mapped_column(
        mysql.BIGINT(unsigned=True),
        ForeignKey("questions.id", ondelete="CASCADE"),
        nullable=False,
    )

    choice_text: Mapped[str] = mapped_column(
        Text,
        nullable=False,
    )

    is_correct: Mapped[bool] = mapped_column(
        Boolean,
        nullable=False,
        server_default=text("0"),
    )

    question: Mapped[Question] = relationship(
        back_populates="choices",
    )

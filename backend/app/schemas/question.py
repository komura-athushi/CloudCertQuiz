from pydantic import BaseModel, ConfigDict


class ChoiceResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    choice_text: str


# 質問のレスポンスモデル
# APIのレスポンスとして、返したくないフィールドもあるため、Questionモデルをそのまま返すのではなく、QuestionResponseを定義している
class QuestionResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    choices: list[ChoiceResponse]


class ChoiceAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    choice_text: str
    is_correct: bool


class QuestionAnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    question_text: str
    explanation: str | None
    choices: list[ChoiceAnswerResponse]


class AnswerResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    question_id: int
    selected_choice_id: int
    is_correct: bool
    question: QuestionAnswerResponse

import datetime
# field_validator: 빈 문자열 허용 안되게 함
from pydantic import BaseModel, field_validator
from domain.user.user_schema import User


class AnswerCreate(BaseModel):
    content: str


    # AnswerCreate 스키마에 content 값이 저장될 때 실행된다.
    @field_validator('content')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v

class Answer(BaseModel):
    id: int
    content: str
    create_date: datetime.datetime
    user: User | None
    question_id: int
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

class AnswerUpdate(AnswerCreate):
    answer_id: int

class AnswerDelete(BaseModel):
    answer_id: int


class AnswerVote(BaseModel):
    answer_id: int
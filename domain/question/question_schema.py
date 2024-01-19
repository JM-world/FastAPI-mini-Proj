import datetime

from pydantic import BaseModel, field_validator

from domain.answer.answer_schema import Answer
from domain.user.user_schema import User

class Question(BaseModel):
    id: int
    subject: str    # subject: str | None = None 은 null 가능
    content: str
    create_date: datetime.datetime
    answers: list[Answer] = []
    user: User | None
    modify_date: datetime.datetime | None = None
    voter: list[User] = []

class QuestionCreate(BaseModel):
    subject: str
    content: str

    @field_validator('subject')
    def not_empty1(cls, v):
        if not v or not v.strip():
            raise ValueError('제목을 입력해주세요.')
        return v

    @field_validator('content')
    def not_empty2(cls, w):
        if not w or not w.strip():
            raise ValueError('내용을 입력해주세요.')
        return w

class QuestionList(BaseModel):
    total: int = 0
    question_list: list[Question] = []

class QuestionUpdate(QuestionCreate):
    question_id: int

class QuestionDelete(BaseModel):
    question_id: int

class QuestionVote(BaseModel):
    question_id: int
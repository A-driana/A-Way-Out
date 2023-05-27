from pydantic import BaseModel
from datetime import datetime


class Register(BaseModel):
    username: str
    password: str
    email: str
    is_admin: bool | None = False

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'username': 'hopeless',
                'password': '<your_password>',
                'email': 'hopeless@gmail.com',
                'is_admin': False
            }
        }


class RegisterRes(BaseModel):
    username: str
    email: str

    class Config:
        orm_mode = True


class UpdateUserSchema(RegisterRes):
    pass


class LogIn(BaseModel):
    username: str
    password: str


class TodoSchema(BaseModel):
    title: str
    completed: bool | None = False
    end_date: datetime | None = None
    reminder: datetime | None = None

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'title': 'Do something with your life!',
                'completed': False,
                'end_date': '2023-05-31T23:59:00.478014',
                'reminder': '2023-05-28T20:00:00.478014',

            }
        }


class TodoResponse(BaseModel):
    id: int
    title: str
    completed: bool
    end_date: datetime
    reminder: datetime
    last_updated: datetime
    date_added: datetime
    user_id: int

    class Config:
        orm_mode = True
        schema_extra = {
            'example': {
                'id': 2,
                'title': 'Do something with your life!',
                'completed': False,
                'end_date': '2023-05-31T23:59:00.478014',
                'reminder': '2023-05-28T20:00:00.478014',
                'last_updated': '2023-05-18T20:30:30.370939',
                'date_added': '2023-05-18T20:30:30.370939',
                'user_id': 5
            }
        }


email_ls = ["somethingcool@gmail.com"]


class EmailSchema(BaseModel):
    email: list[str] | None = email_ls

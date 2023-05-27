from app.db import Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, Integer, String, DateTime, Text, Boolean, ForeignKey
import datetime as _date


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, primary_key=True)
    username = Column(String(30), unique=True)
    password = Column(Text, nullable=True)
    email = Column(String, unique=True)
    is_admin = Column(Boolean, default=False)

    todos = relationship('TodoDB', back_populates='user', cascade='all, delete, delete-orphan', passive_deletes=True)

    def __repr__(self):
        return f'< User {self.username}'


class TodoDB(Base):
    __tablename__ = 'Todos'

    id = Column(Integer, primary_key=True)
    title = Column(String)
    completed = Column(Boolean, default=False)
    end_date = Column(DateTime, nullable=True)
    reminder = Column(DateTime, nullable=True)
    last_updated = Column(DateTime, default=_date.datetime.utcnow)
    date_added = Column(DateTime, default=_date.datetime.utcnow)
    sent_alert = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('User.id', ondelete='CASCADE'))

    todos = relationship('Notification', back_populates='todo', cascade='all, delete, delete-orphan',
                         passive_deletes=True)
    user = relationship('User', back_populates='todos')

    def __repr__(self):
        return f'<Title: {self.title}'


class Notification(Base):
    __tablename__ = 'Notification'

    id = Column(Integer, primary_key=True)
    message = Column(String)
    user_id = Column(Integer)
    todo_id = Column(Integer, ForeignKey('Todos.id', ondelete='CASCADE'))

    todo = relationship('TodoDB', back_populates='todos')

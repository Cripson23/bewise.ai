from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class QuestionsModel(db.Model):
    __tablename__ = 'Questions'

    id = db.Column(db.Integer, unique=True, nullable=False, primary_key=True)
    question = db.Column(db.String(), unique=True, nullable=False)
    answer = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, question, answer, created_at):
        self.question: str = question
        self.answer: str = answer
        self.created_at: datetime = created_at

    def __repr__(self):
        return f""

    def to_dict(self):
        question: dict = {
            'question': self.question,
            'answer': self.answer,
            'created_at': self.created_at
        }
        return question

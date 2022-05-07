import os

import logging
from logging.config import dictConfig
import requests
from datetime import datetime

from flask import Flask, jsonify, request, abort
from flask_cors import CORS, cross_origin
from flask_migrate import Migrate

from models import db, QuestionsModel

dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'formatter': 'default'
    }},
    'root': {
        'level': 'DEBUG',
        'handlers': ['wsgi']
    }
})

app = Flask(__name__)
cors = CORS(app)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)
logger = logging.getLogger()


def get_questions_from_api(num: int) -> list:
    r = requests.get(f"https://jservice.io/api/random?count={num}")
    return r.json()


@app.route("/questions", methods=['POST'])
def questions():
    data: dict = request.json
    if not data or 'questions_num' not in data:
        abort(400)

    try:
        questions_num = int(data['questions_num'])
    except ValueError:
        return jsonify({'error': 'type error for questions_num value'})
    finally:
        logger.debug(request.headers)

    if questions_num < 1 or questions_num > 100:
        return jsonify({'error': 'invalid value'})

    questions_json: list = get_questions_from_api(questions_num)

    count_add_questions: int = 0
    last_add_question = None
    # Цикл по всем полученным вопросам
    for question in questions_json:
        question_text: str = question['question']
        answer: str = question['answer']

        ques = QuestionsModel.query.filter_by(question=question_text, answer=answer).first()
        # Если вопрос не найден в базе данных и не пустые текст вопроса и ответ, добавляем
        if ques is None and (len(question_text) > 0 and len(answer) > 0):
            new_question = QuestionsModel(question=question_text, answer=answer,
                                          created_at=datetime.now())

            db.session.add(new_question)
            db.session.commit()
            last_add_question = new_question.to_dict()
            count_add_questions += 1
        # Если вопрос найден или текст вопроса или ответ пустой, получаем по 1 доп. вопросу,
        # пока не получим уникальный (которого нет в базе), а после добавляем
        else:
            check_add: bool = False
            while not check_add:
                additional_question_json = get_questions_from_api(1)[0]
                additional_question = QuestionsModel.query.filter_by(question=additional_question_json['question'],
                                                                     answer=additional_question_json['answer']).first()
                if additional_question is not None or len(additional_question_json['question']) < 1 or \
                        len(additional_question_json['answer']) < 1:
                    continue
                else:
                    new_question: QuestionsModel = QuestionsModel(question=additional_question_json['question'],
                                                                  answer=additional_question_json['answer'],
                                                                  created_at=datetime.now())
                    db.session.add(new_question)
                    db.session.commit()
                    last_add_question = new_question.to_dict()
                    count_add_questions += 1
                    check_add = True

    logger.info(f"Successfully added to db - {count_add_questions} questions")
    return jsonify(last_add_question)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))

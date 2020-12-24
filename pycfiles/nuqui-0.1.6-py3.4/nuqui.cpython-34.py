# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nuqui/nuqui.py
# Compiled at: 2018-02-13 16:54:30
# Size of source mod 2**32: 4958 bytes
from .dbobjects import User, Score, Question, Meal
from . import SESSION
from random import randint, shuffle
import datetime

def create_user(user_id, user_name):
    session = SESSION()
    user_score = Score(points=0, latest_points=0)
    user = User(id=user_id, name=user_name, score=user_score)
    session.add(user_score)
    session.add(user)
    session.commit()
    session.close()


def remove_user(user_id):
    session = SESSION()
    user = session.query(User).filter_by(id=user_id).one()
    session.delete(user)
    session.commit()
    session.close()


def get_predefined_question_dict_with_random_answers(user_id):
    session = SESSION()
    user = session.query(User).filter_by(id=user_id).one()
    questions_id = user.questions
    all_qustions = session.query(Question).all()
    possible_questions = []
    last_ten_meals = user.meals[-10:]
    if last_ten_meals is not None:
        ingred_last_meals = _get_ingredient_list(last_ten_meals)
        for ing in ingred_last_meals:
            possible_questions.extend(session.query(Question).filter(Question.answer.like('%' + ing + '%')).all())
            possible_questions.extend(session.query(Question).filter(Question.question.like('%' + ing + '%')).all())

    else:
        possible_questions = [question for question in all_qustions if question not in questions_id]
    if not possible_questions:
        possible_questions = all_qustions
    question = possible_questions[randint(0, len(possible_questions) - 1)]
    possible_answers = _get_three_random_answers(question, all_qustions)
    possible_answers.append(question.answer)
    shuffle(possible_answers)
    question_dict = question.to_dictionary()
    question_dict['answer'] = possible_answers
    user.open_question = question
    user.questions.append(question)
    user.open_question_answer = _get_letter_of_answer(question.answer, possible_answers)
    session.commit()
    session.close()
    return question_dict


def _get_ingredient_list(meals):
    """
    :type meals: list of meal objects
    """
    amount_ingredient_list = []
    for meal in meals:
        amount_ingredient_list.extend(meal.food.split(','))

    return amount_ingredient_list


def _get_letter_of_answer(answer, answers_list):
    index = answers_list.index(answer)
    if index == 0:
        return '!A'
    else:
        if index == 1:
            return '!B'
        if index == 2:
            return '!C'
        return '!D'


def _get_three_random_answers(ori_question, all_qustions):
    random_answers_answer = [question.answer for question in all_qustions if question != ori_question]
    return [random_answers_answer[randint(0, len(random_answers_answer) - 1)] for x in range(0, 3)]


def evaluate(answer, user_id):
    session = SESSION()
    user = session.query(User).filter_by(id=user_id).one()
    success = user.open_question_answer == answer
    points = user.open_question.value
    right_answer = user.open_question.answer
    if success:
        user.score.latest_points = points
        user.score.points += points
    total_points = user.score.points
    session.commit()
    session.close()
    return {'success': success, 
     'right_answer': right_answer, 
     'achieved_points': points, 
     'total_points': total_points}


def user_get_open_question(user_id):
    session = SESSION()
    user = session.query(User).filter_by(id=user_id).one()
    session.close()
    if user.open_question is None:
        return
    else:
        return user.open_question.to_dictionary


def add_meal(user_id, food_string, calories):
    session = SESSION()
    meal = Meal(timestamp=datetime.datetime.now(), calories=calories, food=food_string)
    session.add(meal)
    user = session.query(User).filter_by(id=user_id).one()
    user.meals.append(meal)
    session.commit()
    session.close()


def get_score(user_id):
    session = SESSION()
    user = session.query(User).filter_by(id=user_id).one()
    score = user.score
    answer_dict = {'latest_points': score.latest_points, 
     'total_points': score.points}
    session.close()
    return answer_dict
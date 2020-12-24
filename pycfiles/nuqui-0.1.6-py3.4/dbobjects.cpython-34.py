# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-x86_64/egg/nuqui/dbobjects.py
# Compiled at: 2018-02-09 10:53:48
# Size of source mod 2**32: 2534 bytes
from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
Base = declarative_base()
User_question = Table('user_question', Base.metadata, Column('user_id', Integer, ForeignKey('user.id')), Column('question_id', Integer, ForeignKey('downloaded_question.id')))
User_meal = Table('user_meal', Base.metadata, Column('user_id', Integer, ForeignKey('user.id')), Column('meal_id', Integer, ForeignKey('meal.id')))
User_open_question = Table('user_open_question', Base.metadata, Column('user_id', Integer, ForeignKey('user.id')), Column('question_id', Integer, ForeignKey('downloaded_question.id'), nullable=True))

class Question(Base):
    __tablename__ = 'downloaded_question'
    id = Column(Integer, primary_key=True)
    answer = Column(String)
    question = Column(String)
    value = Column(Integer)

    def to_dictionary(self):
        return {'id': self.id, 
         'question': self.question, 
         'answer': self.answer, 
         'value': self.value}


class User(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    score = relationship('Score', uselist=False, cascade='delete')
    questions = relationship('Question', secondary=User_question, cascade='delete')
    meals = relationship('Meal', secondary=User_meal, cascade='delete')
    open_question = relationship('Question', uselist=False, secondary=User_open_question)
    open_question_answer = Column(String, nullable=True)

    def to_dictionary(self):
        return {'id': self.id, 
         'name': self.name, 
         'points': self.score.points, 
         'latest_points': self.score.latest_points, 
         'questions': self.questions}


class Score(Base):
    __tablename__ = 'score'
    id = Column(Integer, primary_key=True)
    points = Column(Integer)
    latest_points = Column(Integer)
    user_id = Column(Integer, ForeignKey('user.id'))


class Meal(Base):
    __tablename__ = 'meal'
    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime)
    calories = Column(Integer)
    food = Column(String)

    def to_dictionary(self):
        return {'id': self.id, 
         'timestamp': self.timestamp, 
         'calories': self.calories, 
         'food': self.food}


# global Base ## Warning: Unused global
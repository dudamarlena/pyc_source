# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/meritocracy/models.py
# Compiled at: 2009-03-20 16:48:59
from sqlalchemy import orm, Column
from sqlalchemy.types import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relation
from meritocracy import meta
Base = declarative_base(metadata=meta.metadata)

def init_model(engine):
    """Required to set up the models"""
    sm = orm.sessionmaker(autoflush=True, autocommit=True, bind=engine)
    meta.engine = engine
    meta.Session = orm.scoped_session(sm)


class Repository(Base):
    __tablename__ = 'repositories'
    id = Column(Integer, primary_key=True)
    path = Column(String(500), unique=True, nullable=False)
    current_revision = Column(String(40), nullable=False)


class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(500), unique=True)


class UserEmail(Base):
    __tablename__ = 'useremails'
    user_id = Column(Integer, ForeignKey('users.id'))
    email = Column(String(500), primary_key=True)


class Contribution(Base):
    __tablename__ = 'contributions'
    id = Column(Integer, primary_key=True)
    revision = Column(String(40), nullable=False)
    repo_id = Column(Integer, ForeignKey('repositories.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
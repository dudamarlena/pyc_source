# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\app\database.py
# Compiled at: 2015-08-19 15:30:26
# Size of source mod 2**32: 803 bytes
"""database.py: Sets up the database."""
__author__ = 'dan'
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from flask import current_app
testing = current_app.config['SQLALCHEMY_DATABASE_URI']
engine = create_engine(current_app.config['SQLALCHEMY_DATABASE_URI'], convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    from .account import models
    from .blog import models
    from .core import models
    Base.metadata.create_all(bind=engine)
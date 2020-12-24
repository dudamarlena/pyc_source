# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/flaskapp/base/database.py
# Compiled at: 2019-07-24 05:34:04
# Size of source mod 2**32: 753 bytes
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
engine = create_engine('sqlite:////tmp/{PROJECT_NAME}.db', convert_unicode=True)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False,
  bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()

def init_db():
    import models
    Base.metadata.create_all(bind=engine)


init_db()
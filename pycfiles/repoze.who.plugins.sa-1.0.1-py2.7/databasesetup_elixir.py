# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/databasesetup_elixir.py
# Compiled at: 2011-05-02 14:52:14
"""Stuff required to setup the test database."""
import os
from sqlalchemy import *
from sqlalchemy.orm import *
from cStringIO import StringIO
from cgi import FieldStorage
import elixir
from fixture.elixir_model import init_model, DBSession, metadata, User
engine = create_engine(os.environ.get('DBURL', 'sqlite://'))

def setup_database():
    init_model(engine)
    teardownDatabase()
    elixir.setup_all(True)
    user = User()
    user.user_name = 'rms'
    user.password = 'freedom'
    DBSession.add(user)
    user = User()
    user.user_name = 'linus'
    user.password = 'linux'
    DBSession.add(user)
    user = User()
    user.user_name = 'sballmer'
    user.password = 'developers'
    DBSession.add(user)
    user = User()
    user.user_name = 'guido'
    user.password = 'phytonic'
    DBSession.add(user)
    user = User()
    user.user_name = 'rasmus'
    user.password = 'php'
    DBSession.add(user)
    DBSession.commit()


def teardownDatabase():
    DBSession.rollback()
    metadata.drop_all(engine)
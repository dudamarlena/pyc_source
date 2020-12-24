# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/databasesetup.py
# Compiled at: 2011-11-29 15:47:41
"""Stuff required to setup the test database."""
import os
from sqlalchemy import *
from sqlalchemy.orm import *
from cStringIO import StringIO
from cgi import FieldStorage
from fixture.model import init_model, DBSession, metadata, Permission, Group, User
engine = create_engine(os.environ.get('DBURL', 'sqlite://'))

def setup_database():
    init_model(engine)
    teardownDatabase()
    metadata.create_all(engine)
    see_site = Permission()
    see_site.permission_name = 'see-site'
    DBSession.add(see_site)
    edit_site = Permission()
    edit_site.permission_name = 'edit-site'
    DBSession.add(edit_site)
    commit = Permission()
    commit.permission_name = 'commit'
    DBSession.add(commit)
    admins = Group('admins')
    admins.permissions.append(edit_site)
    DBSession.add(admins)
    developers = Group('developers')
    developers.permissions = [commit, edit_site]
    DBSession.add(developers)
    trolls = Group('trolls')
    trolls.permissions.append(see_site)
    DBSession.add(trolls)
    php = Group('php')
    DBSession.add(php)
    python = Group('python')
    DBSession.add(python)
    user = User()
    user.user_name = 'rms'
    user.password = 'freedom'
    user.groups.append(admins)
    user.groups.append(developers)
    DBSession.add(user)
    user = User()
    user.user_name = 'linus'
    user.password = 'linux'
    user.groups.append(developers)
    DBSession.add(user)
    user = User()
    user.user_name = 'sballmer'
    user.password = 'developers'
    user.groups.append(trolls)
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
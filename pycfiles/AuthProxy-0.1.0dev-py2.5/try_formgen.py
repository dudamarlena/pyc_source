# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/authproxy/lib/try_formgen.py
# Compiled at: 2005-08-02 12:47:03
from sqlalchemy import *
from sqlalchemy.orm import *
from formalchemy import FieldSet
meta = MetaData()
user_table = Table('users', meta, Column('email', Unicode(40), primary_key=True), Column('name', Unicode(20)), Column('active', Boolean, default=True))

class User(object):
    pass


mapper(User, user_table)
user = User()
print FieldSet(user).render()
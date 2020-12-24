# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/model/Administrator.py
# Compiled at: 2008-03-03 12:14:37
from sqlalchemy import Table, Column, Integer, String, CheckConstraint

class Administrator(object):

    def __repr__(self):
        return '<Administrator(%s %s)>' % (self.login_name, self.email)


def get_administrators_table(meta):
    administrators_table = Table('administrators', meta, Column('id', Integer, primary_key=True), Column('login_name', String(30), nullable=False, unique=True), Column('password_hash', String(64), CheckConstraint('length("password_hash") = 64'), nullable=False), Column('email', String(50), nullable=False, unique=True), mysql_engine='InnoDB')
    return administrators_table
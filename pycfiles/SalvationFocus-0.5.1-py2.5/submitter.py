# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/model/Submitter.py
# Compiled at: 2008-03-03 12:14:02
from sqlalchemy import Table, Column, Integer, String, UniqueConstraint

class Submitter(object):

    def __repr__(self):
        return '<Submitter(%s %s)>' % (self.first_name, self.last_name)


def get_submitters_table(meta):
    submitters_table = Table('submitters', meta, Column('id', Integer, primary_key=True), Column('first_name', String(30), nullable=False), Column('last_name', String(30), nullable=False), Column('phone', String(12), nullable=False), Column('email', String(50), nullable=False), UniqueConstraint('first_name', 'last_name'), mysql_engine='InnoDB')
    return submitters_table
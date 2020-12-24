# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/model/Believer.py
# Compiled at: 2008-03-03 12:13:49
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, UniqueConstraint

class Believer(object):

    def __repr__(self):
        return '<Believer(%s %s)>' % (self.first_name, self.last_name)


def get_believers_table(meta):
    believers_table = Table('believers', meta, Column('id', Integer, primary_key=True), Column('first_name', String(30), nullable=False), Column('last_name', String(30), nullable=False), Column('date_entered', DateTime, nullable=False), Column('last_viewed', DateTime), Column('times_viewed', Integer, default=0), Column('submitter_id', Integer, ForeignKey('submitters.id'), nullable=False), Column('date_answered', DateTime, nullable=False), UniqueConstraint('first_name', 'last_name'), mysql_engine='InnoDB')
    return believers_table
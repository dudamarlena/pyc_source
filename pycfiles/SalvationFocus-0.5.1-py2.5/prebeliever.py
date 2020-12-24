# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salvationfocus/model/Prebeliever.py
# Compiled at: 2008-03-03 13:01:08
from sqlalchemy import Table, Column, Integer, String, ForeignKey, DateTime, UniqueConstraint
from datetime import datetime

class Prebeliever(object):

    def __repr__(self):
        return '<Prebeliever(%s %s)>' % (self.first_name, self.last_name)

    def toDictionary(self):
        prebelieverDict = {}
        prebelieverDict['id'] = self.id
        prebelieverDict['first_name'] = self.first_name
        prebelieverDict['last_name'] = self.last_name
        prebelieverDict['date_entered'] = self.date_entered
        if self.last_viewed != None:
            prebelieverDict['last_viewed'] = self.last_viewed
        else:
            prebelieverDict['last_viewed'] = datetime(1900, 1, 1)
        if self.times_viewed != None:
            prebelieverDict['times_viewed'] = self.times_viewed
        else:
            prebelieverDict['times_viewed'] = 0
        prebelieverDict['submitter_id'] = self.submitter_id
        return prebelieverDict


def get_prebelievers_table(meta):
    prebelievers_table = Table('prebelievers', meta, Column('id', Integer, primary_key=True), Column('first_name', String(30), nullable=False), Column('last_name', String(30), nullable=False), Column('date_entered', DateTime, nullable=False), Column('last_viewed', DateTime), Column('times_viewed', Integer, default=0), Column('submitter_id', Integer, ForeignKey('submitters.id', ondelete='CASCADE'), nullable=False), UniqueConstraint('first_name', 'last_name'), mysql_engine='InnoDB')
    return prebelievers_table
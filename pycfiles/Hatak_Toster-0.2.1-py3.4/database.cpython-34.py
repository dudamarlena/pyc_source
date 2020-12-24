# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/toster/database.py
# Compiled at: 2014-10-11 13:41:36
# Size of source mod 2**32: 1184 bytes
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from haplugin.sql import Base

class TestDatabase(object):

    def __init__(self, settings):
        self.settings = settings

    def recreate_database(self):
        if self.settings['db']['type'] == 'sqlite':
            self.recreate_sqlite_database()
            return
        url = self.settings['db']['testurl']
        engine = create_engine(url)
        connection = engine.connect()
        connection.execute('commit')
        connection.execute('drop database if exists %(db:name)s' % self.settings)
        connection.execute('commit')
        connection.execute('create database %(db:name)s' % self.settings)
        connection.close()

    def recreate_sqlite_database(self):
        try:
            os.unlink(self.settings['db']['name'])
        except FileNotFoundError:
            pass

    def get_engine_and_session(self):
        url = self.settings['db']['url']
        engine = create_engine(url)
        session = sessionmaker(bind=engine)()
        return (engine, session)

    def create_all(self, engine):
        Base.metadata.create_all(engine)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/postgresutils.py
# Compiled at: 2011-01-11 00:48:50
"""A set of simple utilities to manage the postgres database 

associated with this code."""
from sqlalchemy import create_engine, Table, Column, Integer, String, MetaData
from sqlalchemy.orm import sessionmaker, mapper
from conf import settings
import os

class Employee(object):

    def __init__(self, name, fullname, password):
        self.name = name
        self.fullname = fullname
        self.password = password

    def __repr__(self):
        return "<Employee('%s','%s', '%s')>" % (self.name, self.fullname, self.password)


class Utils:
    """Contains some utility methods for a Postgres database"""

    def __init__(self):
        self.metadata = MetaData()
        self.synthesis_engine = create_engine('postgresql+psycopg2://%s:%s@%s:%s/%s' % (settings.DB_USER, settings.DB_PASSWD, settings.DB_HOST, settings.DB_PORT, settings.DB_DATABASE), echo=settings.DEBUG_DB)
        self.synthesis_metadata = MetaData(self.synthesis_engine)
        Session = sessionmaker(bind=self.synthesis_engine, autoflush=True)
        self.session = Session()
        if settings.DEBUG:
            print 'postgresutils.Utils inititalized'

    def blank_table(self):
        self.employee_table.drop(bind=self.synthesis_engine)
        self.session.commit()
        print 'cleared the employee_table table'

    def create_database(self, databaseName):
        if not databaseName == '':
            parameters = ['--host=localhost', '--username=%s' % settings.DB_USER, settings.DB_DATABASE, 'Synthesis Project Database for %s' % settings.MODE]
            compileCommand = '/usr/bin/createdb'
            if settings.DEBUG:
                print 'creating db with command: %s %s' % (compileCommand, parameters)
            rc = os.spawnv(os.P_WAIT, compileCommand, parameters)
            return rc
        raise

    def create_test_table(self):
        self.employee_table = Table('employee', self.metadata, Column('id', Integer, primary_key=True), Column('name', String(40)), Column('fullname', String(100)), Column('password', String(15)))
        mapper(Employee, self.employee_table)
        self.metadata.create_all(bind=self.synthesis_engine)
        self.session.commit()
        print 'created the employee table'

    def blank_database(self):
        self.synthesis_metadata.reflect()
        for table in reversed(self.synthesis_metadata.sorted_tables):
            print table, 'found'
            table.drop(checkfirst=True)
            print 'dropped', table

        print 'all tables dropped'


if __name__ == '__main__':
    utils = Utils()
    print 'uncomment the things you want to run, or else nothing will happen'
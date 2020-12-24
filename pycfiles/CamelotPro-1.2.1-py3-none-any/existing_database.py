# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/test/snippet/existing_database.py
# Compiled at: 2013-04-11 17:47:52
from sqlalchemy.engine import create_engine
from sqlalchemy.pool import StaticPool
engine = create_engine('sqlite:///test.sqlite')
connection = engine.connect()
try:
    connection.execute('drop table person')
except:
    pass

connection.execute('create table person ( pk INTEGER PRIMARY KEY,\n                                             first_name TEXT NOT NULL,\n                                             last_name TEXT NOT NULL )')
connection.execute('insert into person (first_name, last_name)\n                       values ("Peter", "Principle")')
from camelot.admin.entity_admin import EntityAdmin
from camelot.core.sql import metadata
from sqlalchemy.schema import Table
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base(metadata=metadata)

class Person(Base):
    __table__ = Table('person', Base.metadata, autoload=True, autoload_with=engine)

    class Admin(EntityAdmin):
        list_display = [
         'first_name', 'last_name']


from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section
from camelot.core.conf import settings

class AppAdmin(ApplicationAdmin):

    def get_sections(self):
        return [
         Section('All tables', self, items=[Person])]


class Settings(object):

    def ENGINE(self):
        return engine

    def setup_model(self):
        metadata.bind = engine


settings.append(Settings())
app_admin = AppAdmin()
if __name__ == '__main__':
    from camelot.view.main import main
    main(app_admin)
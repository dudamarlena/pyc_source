# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/sahriswiki/dbm.py
# Compiled at: 2011-02-12 01:51:28
"""DataBase Manager

...
"""
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from circuits import handler, BaseComponent, Event
import schema
metadata = MetaData()
Base = declarative_base(metadata=metadata)

class DatabaseLoaded(Event):
    """Database Loaded Event"""
    pass


class DatabaseManager(BaseComponent):

    def __init__(self, dburi, echo=False, convert_unicode=True):
        super(DatabaseManager, self).__init__()
        self.engine = create_engine(dburi, echo=echo, convert_unicode=convert_unicode)
        self.session = scoped_session(sessionmaker(bind=self.engine, autoflush=True, autocommit=False))

    @handler('registered')
    def _on_registered(self, component, manager):
        if component == self:
            tables = self.engine.table_names()
            for (Table, data) in schema.DATA:
                if Table.__tablename__ not in tables:
                    Table.__table__.create(self.engine)
                    for row in data:
                        self.session.add(Table(*row))

                    self.session.commit()

            metadata.create_all(self.engine)

    @handler('stopped', target='*')
    def _on_stopped(self, component):
        self.session.flush()
        self.session.commit()
        self.session.close()
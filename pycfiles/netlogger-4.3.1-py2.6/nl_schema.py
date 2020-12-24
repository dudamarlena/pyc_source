# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/analysis/schema/nl_schema.py
# Compiled at: 2011-01-18 18:36:28
"""
Contains the code to create and map objects to he generic 'NetLogger' schema
via a SQLAlchemy interface.
"""
__rcsid__ = '$Id: nl_schema.py 26983 2011-01-18 23:36:28Z dang $'
__author__ = 'Dan Gunter <dkgunter@lbl.gov>'
import logging
from netlogger.analysis.schema._base import SABase
from sqlalchemy import *
from sqlalchemy import orm, exceptions
from netlogger.nllog import get_logger

class Event(SABase):
    """Main table.
    """
    pass


class Identifier(SABase):
    """Identifiers.
    """
    pass


class Value(SABase):
    """Everything else.
    """
    pass


def init_db(db, metadata, **kw):
    """
    Function to create the schema and/or
    connect and set up object mappings.
    
    @type   db: SQLAlch db/engine object.
    @param  db: Engine object to initialize.
    @type   metadata: SQLAlch metadata object.
    @param  metadata: Associated metadata object to initialize.
    """
    log = get_logger('nl_schema')
    _dbg = log.isEnabledFor(logging.DEBUG)
    if db.name == 'mysql':
        KeyInt = BigInteger
    else:
        KeyInt = Integer
    tbl = Table('event', metadata, Column('event_id', KeyInt, primary_key=True), Column('ts', NUMERIC(precision=16, scale=6)), Column('event', VARCHAR(255)), Column('level', SmallInteger), Column('startend', SmallInteger), Column('status', Integer, nullable=True))
    orm.mapper(Event, tbl, properties={'identifiers': orm.relation(Identifier, backref='event'), 
       'values': orm.relation(Value, backref='event')})
    tbl = Table('ident', metadata, Column('id', KeyInt, primary_key=True), Column('event_id', KeyInt, ForeignKey('event.event_id'), nullable=False), Column('name', VARCHAR(255)), Column('value', VARCHAR(255)))
    orm.mapper(Identifier, tbl)
    tbl = Table('value', metadata, Column('id', KeyInt, primary_key=True), Column('event_id', KeyInt, ForeignKey('event.event_id'), nullable=False), Column('name', VARCHAR(255)), Column('value', VARCHAR(255)))
    orm.mapper(Value, tbl)
    metadata.create_all(db)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/hmiscsv27writer.py
# Compiled at: 2010-12-12 18:24:12
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date
import conf.settings, clsexceptions, dbobjects
from writer import Writer

class HMISCSV27Writer(dbobjects.DatabaseObjects):
    implements(Writer)

    def __init__(self):
        pass
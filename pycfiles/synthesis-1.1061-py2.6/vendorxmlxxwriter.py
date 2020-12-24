# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/synthesis/vendorxmlxxwriter.py
# Compiled at: 2010-12-12 18:24:12
import os.path, interpretpicklist
from datetime import timedelta, date, datetime
from time import strptime, time
from xmlutilities import IDGeneration
from sqlalchemy import create_engine, Table, Column, Numeric, Integer, String, Boolean, MetaData, ForeignKey, Sequence
from sqlalchemy.orm import sessionmaker, mapper, backref, relation, clear_mappers
from sqlalchemy.types import DateTime, Date
from sys import version
from conf import settings
import clsexceptions, dbobjects
from writer import Writer
from zope.interface import implements

class VendorXMLXXWriter(dbobjects.DatabaseObjects):
    implements(Writer)

    def __init__(self):
        pass
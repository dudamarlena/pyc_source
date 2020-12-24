# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/logservice/models/meta.py
# Compiled at: 2016-09-07 16:13:36
# Size of source mod 2**32: 904 bytes
import sys
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.schema import MetaData
from sqlalchemy import func, Column, DateTime, String
import uuid
NAMING_CONVENTION = {'ix': 'ix_%(column_0_label)s', 
 'uq': 'uq_%(table_name)s_%(column_0_name)s', 
 'ck': 'ck_%(table_name)s_%(constraint_name)s', 
 'fk': 'fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s', 
 'pk': 'pk_%(table_name)s'}
if 'unittest' in sys.modules.keys():
    NAMING_CONVENTION = {}
metadata = MetaData(naming_convention=NAMING_CONVENTION)
Base = declarative_base(metadata=metadata)
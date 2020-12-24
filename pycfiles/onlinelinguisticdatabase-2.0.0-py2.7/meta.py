# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/onlinelinguisticdatabase/model/meta.py
# Compiled at: 2016-09-19 13:27:02
"""SQLAlchemy Metadata and Session object"""
import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from onlinelinguisticdatabase.model.model import Model
__all__ = [
 'Base', 'Session', 'now']
Session = scoped_session(sessionmaker())
Base = declarative_base(cls=Model)

def now():
    return datetime.datetime.utcnow()
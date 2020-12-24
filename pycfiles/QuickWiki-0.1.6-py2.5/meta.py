# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/quickwiki/model/meta.py
# Compiled at: 2009-02-23 12:50:50
"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
__all__ = [
 'Session', 'engine', 'metadata']
engine = None
Session = scoped_session(sessionmaker())
metadata = MetaData()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/model/meta.py
# Compiled at: 2010-08-08 03:18:44
"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
__all__ = [
 'Session', 'metadata', 'Base']
Session = scoped_session(sessionmaker())
metadata = MetaData()
Base = declarative_base()
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/model/meta.py
# Compiled at: 2011-02-18 19:15:08
"""SQLAlchemy Metadata and Session object"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
__all__ = [
 'Base', 'Session']
Session = scoped_session(sessionmaker())
Base = declarative_base()
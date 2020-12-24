# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesitetemplate/template/+package+/model/meta.py
# Compiled at: 2008-11-02 14:59:52
"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
__all__ = [
 'Session', 'metadata']
engine = None
Session = None
metadata = MetaData()
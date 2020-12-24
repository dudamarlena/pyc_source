# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/zeta/model/meta.py
# Compiled at: 2010-02-11 06:42:11
"""SQLAlchemy Metadata and Session object"""
from sqlalchemy import MetaData
from sqlalchemy.orm import scoped_session, sessionmaker
__all__ = [
 'engine', 'Session', 'metadata', 'tbl_mappers']
engine = None
Session = None
tbl_mappers = {}
wiki_tables = {}
wikipage_factory = {}
sysentries_cfg = {}
authkit_initialized = False
userscomp = None
metadata = MetaData()
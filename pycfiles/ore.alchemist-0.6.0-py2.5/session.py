# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/alchemist/session.py
# Compiled at: 2008-09-11 20:29:53
"""

how do we access the current session in use.

from ore.alchemist import Session
session = Session()
assert session is Session()

"""
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.scoping import ScopedSession
import manager

class TransactionScoped(ScopedSession):

    def __call__(self, **kwargs):
        session = super(TransactionScoped, self).__call__(**kwargs)
        if not session.joined:
            data_manager = manager.SessionDataManager(session)
            data_manager.register()
            session.joined = True
        if not session.transaction:
            session.begin()
        return session


def _zope_session(session_factory):

    class ZopeSession(session_factory):
        joined = False

        def __init__(self, **kwargs):
            super(ZopeSession, self).__init__(**kwargs)

    return ZopeSession


Session = TransactionScoped(_zope_session(sessionmaker(autoflush=True, transactional=True)))
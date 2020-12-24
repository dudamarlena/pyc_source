# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/repl/dispatcher.py
# Compiled at: 2010-08-27 06:32:04
import random, datetime
from zope.interface import implements
from zope.component import getUtility
from zope.password.interfaces import IPasswordManager
from interfaces import IDispatcher
from session import Session

class Dispatcher:
    implements(IDispatcher)
    _nextid = None
    _sessions = {}
    _credentials = {}
    _pwd_manager = 'SSHA'

    def _authenticate(self, id, pwd):
        try:
            pm = getUtility(IPasswordManager, name=self._pwd_manager)
            return pm.checkPassword(self._credentials[id], pwd)
        except KeyError:
            return False

    def _generate_id(self):
        while True:
            if self._nextid is None:
                self._nextid = random.randrange(0, 2147483648)
            id = self._nextid
            self._nextid += 1
            if id not in self._credentials.keys():
                return id
            self._nextid = None

        return

    def _generate_password(self):
        now = ('').join(datetime.datetime.now().ctime().split())
        chars = []
        for i in range(30):
            chars.extend(random.sample(now, 1))

        return ('').join(chars)

    def set_session(self, context):
        id = self._generate_id()
        pwd = self._generate_password()
        pm = getUtility(IPasswordManager, name=self._pwd_manager)
        self._credentials[id] = pm.encodePassword(pwd)
        self._sessions[id] = Session(context)
        return (id, pwd)

    def get_session(self, id, password):
        if self._authenticate(id, password):
            return self._sessions[id]
        else:
            return

    def del_session(self, id, password):
        if self._authenticate(id, password):
            del self._sessions[id]
            del self._credentials[id]

    def clean(self):
        self._sessions = {}
        self._credentials = {}
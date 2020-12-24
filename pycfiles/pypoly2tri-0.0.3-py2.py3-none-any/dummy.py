# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pypoly/http/auth/dummy.py
# Compiled at: 2011-11-24 06:31:21
__doc__ = '\nWarning: Only use the dummy authentication for development purpose.\n'
import pypoly, pypoly.session
from pypoly.component.plugin import AuthPlugin

class Main(object):

    def init(self):
        pass

    def start(self):
        pypoly.plugin.register(DummyAuth)


class DummyAuth(AuthPlugin):
    """
    This is a dummy authentication.

    :since: 0.4
    """

    def __init__(self):
        AuthPlugin.__init__(self)
        self._passwords = {}

    def login(self, username, password):
        """
        Verifies credentials for username and password.
        """
        tmp = [ g.strip() for g in password.split(',') ]
        if len(tmp) > 1:
            pypoly.session.set('groups', tmp)
            self._passwords[username] = password
            return True
        return False

    def get_groups(self, username):
        if pypoly.user.get_username() == None:
            return []
        else:
            return pypoly.session.get('groups', [])
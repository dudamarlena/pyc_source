# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/fixture/pylonsapp.py
# Compiled at: 2009-03-16 12:29:20
"""
Fake controller-only Pylons application.

"""
from pylons import response
from pylons.controllers import WSGIController
from repoze.what.predicates import All, Not, not_anonymous, is_user, in_group
from repoze.what.plugins.pylonshq import ActionProtector, ControllerProtector, is_met, not_met
from tests.fixture import special_require

class SubController1(WSGIController):
    """Mock Pylons subcontroller"""

    def index(self):
        return 'hello sub1'

    def in_group(self):
        return 'in group'


class SecurePanel(WSGIController):
    """Mock Pylons secure controller"""

    def index(self):
        return 'you are in the panel'

    @ActionProtector(in_group('developers'))
    def commit(self):
        return 'you can commit'


SecurePanel = ControllerProtector(in_group('admins'))(SecurePanel)

class SecurePanelWithHandler(WSGIController):
    """Mock Pylons secure controller"""

    def index(self):
        return 'you are in the panel with handler'

    @staticmethod
    def sorry(reason):
        response.status = 200
        return 'what are you doing here? %s' % reason


SecurePanelWithHandler = ControllerProtector(in_group('admins'), 'sorry')(SecurePanelWithHandler)

class BasicPylonsController(WSGIController):
    """Mock Pylons controller"""
    sub1 = SubController1()
    panel = SecurePanel()

    def index(self, **kwargs):
        return 'hello world'

    @ActionProtector(in_group('admins'))
    def admin(self, *args, **kwargs):
        return 'got to admin'

    def troll_detected(reason):
        return 'Trolls are banned'

    @ActionProtector(All(not_anonymous(), Not(is_user('sballmer'))), denial_handler=troll_detected)
    def leave_comment(self):
        return 'Comment accepted'

    @special_require(not_anonymous())
    def logout(self):
        return 'You have been logged out'

    @special_require(All(not_anonymous(), Not(is_user('sballmer'))), denial_handler=troll_detected)
    def start_thread(self):
        return 'You have started a thread'

    @ActionProtector(Not(not_anonymous()))
    def get_parameter(self, something):
        return 'Parameter received: %s' % something

    def boolean_predicate(self):
        p = not_anonymous()
        return 'The predicate is %s' % bool(p)

    def is_met_util(self):
        if is_met(not_anonymous()):
            return 'You are not anonymous'
        return 'You are anonymous'

    def not_met_util(self):
        if not_met(not_anonymous()):
            return 'You are anonymous'
        return 'You are not anonymous'
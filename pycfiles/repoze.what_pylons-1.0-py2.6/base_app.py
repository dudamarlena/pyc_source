# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/base_app.py
# Compiled at: 2009-03-03 13:11:07
"""Stuff required to set up a Pylons/TG2 application for testing."""
import os
from paste import httpexceptions
from paste.registry import RegistryManager
from webtest import TestApp
from beaker.middleware import CacheMiddleware, SessionMiddleware
from pylons.testutil import ControllerWrap, SetupCacheGlobal
from repoze.who.plugins.auth_tkt import AuthTktCookiePlugin
from repoze.what.middleware import setup_auth
from repoze.what.adapters import BaseSourceAdapter
data_dir = os.path.dirname(os.path.abspath(__file__))
session_dir = os.path.join(data_dir, 'session')
default_environ = {'pylons.use_webob': True, 
   'pylons.routes_dict': dict(action='index'), 
   'paste.config': dict(global_conf=dict(debug=True))}

def make_app(controller_klass, environ={}):
    """Creates a `TestApp` instance."""
    app = ControllerWrap(controller_klass)
    app = SetupCacheGlobal(app, environ, setup_cache=True, setup_session=True)
    app = RegistryManager(app)
    app = SessionMiddleware(app, {}, data_dir=session_dir)
    app = CacheMiddleware(app, {}, data_dir=os.path.join(data_dir, 'cache'))
    groups_adapters = {'my_groups': FakeGroupSourceAdapter()}
    permissions_adapters = {'my_permissions': FakePermissionSourceAdapter()}
    cookie = AuthTktCookiePlugin('secret', 'authtkt')
    identifiers = [
     (
      'cookie', cookie)]
    app = setup_auth(app, groups_adapters, permissions_adapters, identifiers=identifiers, authenticators=[], challengers=[], skip_authentication=True)
    app = httpexceptions.make_middleware(app)
    return TestApp(app)


class FakeGroupSourceAdapter(BaseSourceAdapter):
    """Mock group source adapter"""

    def __init__(self):
        super(FakeGroupSourceAdapter, self).__init__()
        self.fake_sections = {'admins': set(['rms']), 
           'developers': set(['rms', 'linus']), 
           'trolls': set(['sballmer']), 
           'python': set(), 
           'php': set()}

    def _find_sections(self, identity):
        username = identity['repoze.who.userid']
        return set([ n for (n, g) in self.fake_sections.items() if username in g
                   ])


class FakePermissionSourceAdapter(BaseSourceAdapter):
    """Mock permissions source adapter"""

    def __init__(self):
        super(FakePermissionSourceAdapter, self).__init__()
        self.fake_sections = {'see-site': set(['trolls']), 
           'edit-site': set(['admins', 'developers']), 
           'commit': set(['developers'])}

    def _find_sections(self, group_name):
        return set([ n for (n, p) in self.fake_sections.items() if group_name in p
                   ])
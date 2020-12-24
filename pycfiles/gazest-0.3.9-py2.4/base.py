# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gazest/lib/base.py
# Compiled at: 2007-10-26 04:45:04
"""The base Controller API

Provides the BaseController class for subclassing, and other objects
utilized by Controllers.
"""
from pylons import c, cache, config, g, request, response, session
from pylons.controllers import WSGIController
from pylons.controllers.util import abort, etag_cache, redirect_to
from pylons.decorators import jsonify, validate
from pylons.i18n import _, ungettext, N_
from pylons.templating import render
from pylons.database import make_session
import gazest.lib.helpers as h, gazest.model as model
from gazest.model import *
from gazest import __version__
from authkit.pylons_adaptors import authorized
from authkit.permissions import RemoteUser, RequestPermission
from pprint import pprint
from datetime import datetime

class BaseController(WSGIController):
    __module__ = __name__

    def __call__(self, environ, start_response):
        model.init_session()
        c.site_readonly = config['site_readonly']
        if not c.site_readonly:
            start = model.Boycott.c.range_start
            stop = model.Boycott.c.range_stop
            expire = model.Boycott.c.expiration_date
            int_ip = h.get_client_int_ip()
            if model.Boycott.query.select(model.and_(start <= int_ip, stop >= int_ip, expire > datetime.utcnow())):
                c.site_readonly = True
        c.request = request
        c.m_info = []
        c.m_warn = []
        c.sidebars = []
        c.routes_dict = request.environ['pylons.routes_dict']
        c.version = __version__
        c.copyright_years = config['copyright_years']
        c.copyright_owner = config['copyright_owner']
        c.copyright_owner_email = config['copyright_owner_email']
        c.nav1_actions = []
        if authorized(RemoteUser()):
            c.nav1_actions.append(('Logout', '/visitor', 'logout'))
        else:
            c.nav1_actions.append(('Login', '/visitor', 'login'))
        c.nav2_actions = [
         ('Home', '/wiki', 'index'), ('About', '/wiki', 'about'), ('Contact', '/home', 'contact'), ('Recent changes', '/wiki', 'recent_changes'), ('Random', '/wiki', 'random_page')]
        if h.has_rank('thaumaturge'):
            c.nav2_actions.append(('Abuse log', '/admin', 'abuse_log'))
        c.nav3_actions = []
        try:
            return WSGIController.__call__(self, environ, start_response)
        finally:
            model.reclaim_session()


__all__ = [ __name for __name in locals().keys() if not __name.startswith('_') or __name == '_' ]
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/esalazar/git/teleceptor/teleceptor/auth.py
# Compiled at: 2014-09-03 00:02:17
"""
    (c) 2014 Visgence, Inc.

    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>
"""
import os, cherrypy
from cherrypy.lib.static import serve_file
from sqlalchemy.orm.exc import NoResultFound
from sessionManager import sessionScope
from models import User
SESSION_KEY = '_cp_username'
PATH = os.path.abspath(os.path.dirname(__file__))

def check_credentials(username, password, session):
    """Verifies credentials for username and password.
    Returns None on success or a string describing the error on failure"""
    try:
        user = session.query(User).filter_by(email=username, password=password).one()
    except NoResultFound:
        return 'Incorrect username or password'

    return


def check_auth(*args, **kwargs):
    """A tool that looks in config for 'auth.require'. If found and it
    is not None, a login is required and the entry is evaluated as a list of
    conditions that the user must fulfill"""
    conditions = cherrypy.request.config.get('auth.require', None)
    if conditions is not None:
        username = cherrypy.session.get(SESSION_KEY)
        if username:
            cherrypy.request.login = username
            for condition in conditions:
                if not condition():
                    raise cherrypy.HTTPRedirect('/auth/login')

        else:
            raise cherrypy.HTTPRedirect('/auth/login')
    return


cherrypy.tools.auth = cherrypy.Tool('before_handler', check_auth)

def require(*conditions):
    """A decorator that appends conditions to the auth.require config
    variable."""

    def decorate(f):
        if not hasattr(f, '_cp_config'):
            f._cp_config = dict()
        if 'auth.require' not in f._cp_config:
            f._cp_config['auth.require'] = []
        f._cp_config['auth.require'].extend(conditions)
        return f

    return decorate


def member_of(groupname):

    def check():
        return cherrypy.request.login == 'joe' and groupname == 'admin'

    return check


def name_is(reqd_username):
    return lambda : reqd_username == cherrypy.request.login


def any_of(*conditions):
    """Returns True if any of the conditions match"""

    def check():
        for c in conditions:
            if c():
                return True

        return False

    return check


def all_of(*conditions):
    """Returns True if all of the conditions match"""

    def check():
        for c in conditions:
            if not c():
                return False

        return True

    return check


class AuthController(object):

    def on_login(self, username):
        """Called on successful login"""
        pass

    def on_logout(self, username):
        """Called on logout"""
        pass

    def loginForm(self, username, msg='Enter login information', from_page='/'):
        return serve_file(PATH + '/login.html', content_type='text/html')

    @cherrypy.expose
    def login(self, username=None, password=None, from_page='/'):
        if username is None or password is None:
            return self.loginForm('', from_page=from_page)
        else:
            with sessionScope() as (s):
                error_msg = check_credentials(username, password, s)
            if error_msg:
                return self.loginForm(username, error_msg, from_page)
            cherrypy.session[SESSION_KEY] = cherrypy.request.login = username
            self.on_login(username)
            raise cherrypy.HTTPRedirect(from_page or '/')
            return

    @cherrypy.expose
    def logout(self, from_page='/'):
        sess = cherrypy.session
        username = sess.get(SESSION_KEY, None)
        sess[SESSION_KEY] = None
        if username:
            cherrypy.request.login = None
            self.on_logout(username)
        raise cherrypy.HTTPRedirect(from_page or '/')
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysvnmanager/controllers/security.py
# Compiled at: 2010-10-07 21:27:24
import logging
from pysvnmanager.lib.base import *
from pylons.i18n import _, ungettext, N_
log = logging.getLogger(__name__)

class SecurityController(BaseController):

    def index(self):
        """
        Show login form. Submits to login/submit
        """
        return render('/login/login.mako')

    def submit(self):
        """
        Verify username and password
        """
        auth_passed = False
        username = request.params.get('username')
        password = request.params.get('password')
        for auth in cfg.auth:
            if auth(username=username, password=password, config=cfg):
                auth_passed = True
                break

        if auth_passed:
            session['user'] = username
            log.info(_('User %s logged in') % session['user'])
            session.save()
            if session.get('path_before_login'):
                redirect(url(session['path_before_login']))
            else:
                redirect(url(controller='check', action='index'))
        else:
            log.error('pySvnManager: User %s login failed from host [%s]' % (username, request.remote_addr))
            session.clear()
            session.save()
            c.login_message = _('Login failed for user: %s') % username
            return render('/login/login.mako')

    def logout(self):
        """
        Logout the user and display a confirmation message
        """
        if 'user' in session:
            log.info(_('User %s logged out') % session['user'])
            del session['user']
            session.save()
        redirect(url('login'))

    def failed(self):
        return render('/auth_failed.mako')
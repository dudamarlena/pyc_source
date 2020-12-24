# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/argonaut/controllers/account.py
# Compiled at: 2011-02-18 19:15:09
import logging
from pylons import request, response, session, tmpl_context as c, url
from pylons.controllers.util import abort, redirect
from argonaut.lib.base import BaseController, render
from repoze.what.predicates import not_anonymous, has_permission
from repoze.what.plugins.pylonshq import ActionProtector
log = logging.getLogger(__name__)

class AccountController(BaseController):

    def login(self):
        """
        This is where the login form should be rendered.
        Without the login counter, we won't be able to tell if the user has
        tried to log in with wrong credentials
        """
        identity = request.environ.get('repoze.who.identity')
        came_from = str(request.GET.get('came_from', '')) or url('/')
        if identity:
            redirect(url(came_from))
        else:
            c.came_from = came_from
            c.login_counter = request.environ['repoze.who.logins'] + 1
            return render('/forms/login.mako')

    @ActionProtector(not_anonymous())
    def welcome(self):
        identity = request.environ.get('repoze.who.identity')
        return 'Welcome user %s' % identity['repoze.who.userid']

    @ActionProtector(not_anonymous())
    def test_user_access(self):
        return 'You are inside user section'

    @ActionProtector(has_permission('Write post'))
    def test_post_access(self):
        return 'You are able to post'
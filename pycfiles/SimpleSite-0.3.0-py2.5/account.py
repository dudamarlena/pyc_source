# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplesite/controllers/account.py
# Compiled at: 2008-11-08 11:13:38
import logging
from pylons import request, response, session, tmpl_context as c
from pylons.controllers.util import abort, redirect_to
from simplesite.lib.base import BaseController, render
import simplesite.lib.helpers as h
log = logging.getLogger(__name__)

class AccountController(BaseController):

    def signin(self):
        if not request.environ.get('REMOTE_USER'):
            abort(401)
        else:
            return render('/derived/account/signedin.html')

    def signout(self):
        return render('/derived/account/signedout.html')

    def signinagain(self):
        request.environ['paste.auth_tkt.logout_user']()
        return render('/derived/account/signin.html').replace('%s', h.url_for('signin'))
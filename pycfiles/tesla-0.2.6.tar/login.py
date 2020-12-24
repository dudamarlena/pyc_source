# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/danjac/petprojects/tesla/tests/output/AuthXpProjectName/authxpprojectname/controllers/login.py
# Compiled at: 2007-09-06 07:54:22
from authxpprojectname.lib.base import *
from authxpprojectname.lib.auth import login, logout

class LoginController(BaseController):
    """A stub example login controller, with login and logout methods"""

    def index(self):
        return 'login_form'

    def signin(self):
        username = request.params.get('username')
        password = request.params.get('password')
        try:
            user = model.User.authenticate(username, password)
            login(user)
            redirect_to('/')
        except model.NotAuthenticated:
            redirect_to(action='index')

    def signout(self):
        logout()
        redirect_to(action='index')
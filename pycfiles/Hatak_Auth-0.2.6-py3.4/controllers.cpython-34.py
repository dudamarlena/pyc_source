# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/auth/controllers.py
# Compiled at: 2015-04-27 17:10:41
# Size of source mod 2**32: 953 bytes
from hatak.controller import Controller
from .forms import LoginForm
from .helpers import LoginFormWidget

class LoginController(Controller):
    template = 'auth:login.jinja2'

    def make(self):
        if self.user.is_logged():
            self.redirect(self.settings['auth_redirect'])
            return
        form = self.add_form(LoginForm, widget=LoginFormWidget)
        if form.validate() is True:
            self.redirect(self.settings['auth_redirect'])
            return
        self.data['login_header'] = self.settings.get('login_header', 'Hatak Auth')


class ForbiddenController(Controller):
    template = 'auth:forbidden.jinja2'

    def make(self):
        if not self.user.is_logged():
            self.redirect('auth:login')


class LogoutController(Controller):
    permissions = [
     ('base', 'view')]

    def make(self):
        self.redirect('auth:login')
        self.session.clear()
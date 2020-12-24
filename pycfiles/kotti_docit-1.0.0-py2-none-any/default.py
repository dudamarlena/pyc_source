# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ubuntu/workspace/kotti_docit/kotti_docit/views/default.py
# Compiled at: 2018-05-30 19:05:27
"""
Created on 2016-01-13
:author: Alteroo Team (oshane@alteroo.com)
"""
from kotti.views import login as kotti_login
from pyramid.view import view_config
from kotti_docit import _
from kotti_docit.views import BaseView

class UserViews(BaseView):

    @view_config(name='password-reset', renderer='kotti_docit:templates/password-reset.pt')
    @view_config(name='request-password-reset', renderer='kotti_docit:templates/password-reset.pt')
    def request_password_reset(self):
        """Password reset view.

        Render the forgot password template and handles its submission and
        rediect to a specific page.
        """
        came_from = self.request.params.get('came_from', self.request.resource_url(self.context))
        login, password = ('', '')
        if 'reset-password' in self.request.POST:
            login = self.request.params['login']
            user = kotti_login._find_user(login)
            if user is not None and user.active:
                return kotti_login.get_settings()['kotti.reset_password_callback'][0](self.request, user)
            self.request.session.flash(_('That username or email is not known by this system.'), 'error')
        return {'url': self.request.application_url + '/@@password-reset', 
           'came_from': came_from, 
           'login': login, 
           'password': password, 
           'register': kotti_login.asbool(kotti_login.get_settings()['kotti.register'])}
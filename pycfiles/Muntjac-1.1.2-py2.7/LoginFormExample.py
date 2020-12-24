# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/form/LoginFormExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout
from muntjac.ui.login_form import LoginForm, ILoginListener

class LoginFormExample(VerticalLayout):

    def __init__(self):
        super(LoginFormExample, self).__init__()
        login = LoginForm()
        login.setWidth('100%')
        login.setHeight('300px')
        login.addListener(NewLoginListener(self), ILoginListener)
        self.addComponent(login)


class NewLoginListener(ILoginListener):

    def __init__(self, c):
        self._c = c

    def onLogin(self, event):
        self._c.getWindow().showNotification('New Login', 'Username: ' + event.getLoginParameter('username') + ', password: ' + event.getLoginParameter('password'))
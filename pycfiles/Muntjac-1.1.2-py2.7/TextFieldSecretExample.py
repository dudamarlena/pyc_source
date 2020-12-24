# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldSecretExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TextField, PasswordField, Button, Alignment
from muntjac.ui.button import IClickListener

class TextFieldSecretExample(VerticalLayout):

    def __init__(self):
        super(TextFieldSecretExample, self).__init__()
        self.setSizeUndefined()
        self.setSpacing(True)
        self._username = TextField('Username')
        self.addComponent(self._username)
        self._password = PasswordField('Password')
        self.addComponent(self._password)
        loginButton = Button('Login', LoginListener(self))
        self.addComponent(loginButton)
        self.setComponentAlignment(loginButton, Alignment.TOP_RIGHT)


class LoginListener(IClickListener):

    def __init__(self, c):
        self._c = c

    def buttonClick(self, event):
        self._c.getWindow().showNotification('User: ' + self._c._username.getValue() + ' Password: ' + self._c._password.getValue())
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/layouts/CustomLayoutsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.ui.custom_layout import CustomLayout
from muntjac.api import VerticalLayout, TextField, PasswordField, Button

class CustomLayoutsExample(VerticalLayout):

    def __init__(self):
        super(CustomLayoutsExample, self).__init__()
        self.setMargin(True)
        custom = CustomLayout('../../sampler/layouts/examplecustomlayout')
        self.addComponent(custom)
        username = TextField()
        custom.addComponent(username, 'username')
        password = PasswordField()
        custom.addComponent(password, 'password')
        ok = Button('Login')
        custom.addComponent(ok, 'okbutton')
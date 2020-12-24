# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/text/TextFieldInputPromptExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TextField, PasswordField, TextArea
from muntjac.data.property import IValueChangeListener

class TextFieldInputPromptExample(VerticalLayout, IValueChangeListener):

    def __init__(self):
        super(TextFieldInputPromptExample, self).__init__()
        self.setSpacing(True)
        self.setMargin(True, False, False, False)
        username = TextField()
        username.setInputPrompt('Username')
        username.setImmediate(True)
        username.addListener(self, IValueChangeListener)
        self.addComponent(username)
        password = PasswordField()
        password.setInputPrompt('Password')
        password.setImmediate(True)
        password.addListener(self, IValueChangeListener)
        self.addComponent(password)
        comment = TextArea()
        comment.setInputPrompt('Comment')
        comment.setRows(3)
        comment.setImmediate(True)
        comment.addListener(self, IValueChangeListener)
        self.addComponent(comment)

    def valueChange(self, event):
        self.getWindow().showNotification('Received ' + str(event.getProperty()))
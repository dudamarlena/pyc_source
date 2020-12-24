# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/ErrorsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Label, VerticalLayout, TextField, FormLayout
from muntjac.terminal.user_error import UserError

class ErrorsExample(VerticalLayout):

    def __init__(self):
        super(ErrorsExample, self).__init__()
        self.setSpacing(True)
        self.addComponent(Label('<h3>Errors in caption</h3>', Label.CONTENT_XHTML))
        self.addComponent(Label("Error indicators are usually placed on the right side of the component's caption."))
        inpt = TextField('Field caption')
        inpt.setComponentError(UserError('This field is never satisfied'))
        self.addComponent(inpt)
        self.addComponent(Label('<h3>Errors without caption</h3>', Label.CONTENT_XHTML))
        self.addComponent(Label('If the component has no caption, the error indicator is usually placed on the right side of the component.'))
        inpt = TextField()
        inpt.setInputPrompt('This field has an error')
        inpt.setComponentError(UserError('This field is never satisfied.'))
        self.addComponent(inpt)
        self.addComponent(Label('<h3>Error icon placement depends on the layout</h3>', Label.CONTENT_XHTML))
        self.addComponent(Label('FormLayout for example places the error between the component caption and the actual field.'))
        fl = FormLayout()
        fl.setMargin(False)
        fl.setSpacing(False)
        self.addComponent(fl)
        inpt = TextField('Field caption')
        inpt.setInputPrompt('This field has an error')
        inpt.setComponentError(UserError('This field is never satisfied.'))
        fl.addComponent(inpt)
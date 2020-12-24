# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/ValidationExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TextField, Label
from muntjac.data.validator import InvalidValueException
from muntjac.data.validators.string_length_validator import StringLengthValidator
from muntjac.data.validators.composite_validator import CompositeValidator
from muntjac.data.validator import IValidator
from muntjac.data.property import IValueChangeListener

class ValidationExample(VerticalLayout):

    def __init__(self):
        super(ValidationExample, self).__init__()
        self._usernames = set()
        self.setSpacing(True)
        pin = TextField('PIN')
        pin.setWidth('50px')
        pin.setImmediate(True)
        self.addComponent(pin)
        pin.addValidator(StringLengthValidator('Must be 4-6 characters', 4, 6, False))
        username = TextField('Username')
        username.setImmediate(True)
        self.addComponent(username)
        usernameValidator = CompositeValidator()
        username.addValidator(usernameValidator)
        usernameValidator.addValidator(StringLengthValidator('Username must be at least 4 characters', 4, 255, False))
        usernameValidator.addValidator(UsernameValidator(self))
        username.addListener(UsernameListener(self), IValueChangeListener)


class UsernameValidator(IValidator):

    def __init__(self, component):
        self._component = component

    def isValid(self, value):
        return value not in self._component._usernames

    def validate(self, value):
        if not self.isValid(value):
            raise InvalidValueException('Username ' + value + ' already in use')


class UsernameListener(IValueChangeListener):

    def __init__(self, component):
        self._component = component

    def valueChange(self, event):
        tf = event.getProperty()
        tf.validate()
        if tf.getValue() is not None:
            self._component._usernames.add(str(tf.getValue()))
            self.addComponent(Label('Added ' + tf.getValue() + ' to usernames'))
        return
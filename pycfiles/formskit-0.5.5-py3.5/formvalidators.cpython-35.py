# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/formvalidators.py
# Compiled at: 2015-07-25 09:04:48
# Size of source mod 2**32: 995 bytes


class FormValidationError(Exception):

    def __init__(self, validator):
        self.validator = validator.__class__.__name__
        self.message = validator.message


class FormValidator(object):
    message = None

    def set_form(self, form):
        self.form = form

    def __call__(self):
        if not self.validate():
            raise FormValidationError(self)


class MustMatch(FormValidator):
    __doc__ = 'Will fail if first values of provided field names are not the same.'
    message = 'input must be the same!'

    def __init__(self, names):
        self.names = names

    def validate(self):
        values = []
        for name in self.names:
            field = self.form.fields[name]
            try:
                values.append(field.values[0].value)
            except IndexError:
                return False

        first = values.pop(0)
        for value in values:
            if first != value:
                return False

        return True
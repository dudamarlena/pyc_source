# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/hgwebcommit/forms.py
# Compiled at: 2011-10-29 00:04:46
from flaskext.wtf import Form
from flaskext.wtf import SelectMultipleField, IntegerField, HiddenField, TextField, SelectField
from flaskext.wtf import TextInput, HiddenInput, Required
from flaskext.babel import lazy_gettext as _

class SizedTextInput(TextInput):

    def __init__(self, size, input_type=None):
        super(SizedTextInput, self).__init__(input_type)
        self.size = size

    def __call__(self, field, **kwargs):
        if 'size' not in kwargs:
            kwargs['size'] = self.size
        return super(SizedTextInput, self).__call__(field, **kwargs)


class SelectFileForm(Form):
    files = SelectMultipleField('Files', validators=[Required()])


class SelectFileConfirmForm(SelectFileForm):
    confirm = IntegerField(widget=HiddenInput())


class SelectFileSubmitConfirmForm(SelectFileConfirmForm):
    operation = HiddenField(validators=[Required()])
    commit_message = TextField(_('Commit message'), widget=SizedTextInput(60))


class SelectActionForm(Form):
    action = SelectField('Action', validators=[Required()])


class ConfirmForm(Form):
    confirm = IntegerField(widget=HiddenInput(), validators=[Required()])
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/haplugin/formskit/models.py
# Compiled at: 2015-01-26 16:41:29
# Size of source mod 2**32: 1079 bytes
from pyramid.session import check_csrf_token
from hatak.unpackrequest import unpack
from formskit import Form
from formskit.formvalidators import FormValidator
from formskit.translation import Translation

class PostForm(Form):

    def __init__(self, request):
        self.request = request
        unpack(self, self.request)
        super().__init__()
        self.add_form_validator(CsrfMustMatch())
        self.init_csrf()

    def reset(self):
        super().reset()
        self.init_csrf()

    def init_csrf(self):
        self.add_field('csrf_token')
        self.set_value('csrf_token', self.session.get_csrf_token())

    def validate(self):
        return super().validate(self.request.POST.dict_of_lists())

    @property
    def translation_class(self):
        return self.settings.get('form_message', Translation)


class CsrfMustMatch(FormValidator):
    message = 'CSRF token do not match!'

    def validate(self):
        self.form.POST['csrf_token'] = self.form.get_value('csrf_token')
        return check_csrf_token(self.form.request, raises=False)
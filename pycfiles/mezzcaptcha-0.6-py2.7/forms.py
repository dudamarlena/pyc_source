# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mezzcaptcha/forms.py
# Compiled at: 2015-04-11 09:11:49
from mezzanine.generic.forms import ThreadedCommentForm
from mezzanine.accounts.forms import ProfileForm
from captcha.fields import CaptchaField

class GuestCommentForm(ThreadedCommentForm):

    def __init__(self, request, *args, **kwargs):
        super(GuestCommentForm, self).__init__(request, *args, **kwargs)
        if not request.user.is_authenticated():
            self.fields['captcha'] = CaptchaField()


class SignUpCaptchaForm(ProfileForm):

    def __init__(self, request, *args, **kwargs):
        super(SignUpCaptchaForm, self).__init__(request, *args, **kwargs)
        self.fields['captcha'] = CaptchaField()
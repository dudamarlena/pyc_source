# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/test_util/fake_captcha.py
# Compiled at: 2010-07-03 06:56:37
from genshi.builder import tag
from trac.core import Component, implements
from trac_captcha.api import CaptchaFailedError, ICaptcha
__all__ = [
 'FakeCaptcha']

class FakeCaptcha(Component):
    implements(ICaptcha)

    def genshi_stream(self, req):
        return tag.div('fake captcha: ' + req.captcha_data.get('old_input', ''))

    def assert_captcha_completed(self, req):
        if req.args.get('fake_captcha') == 'open sesame':
            return
        msg = 'Please fill in the CAPTCHA so we know you are not a spammer.'
        captcha_data = dict(old_input=req.args.get('fake_captcha', ''))
        raise CaptchaFailedError(msg, captcha_data)
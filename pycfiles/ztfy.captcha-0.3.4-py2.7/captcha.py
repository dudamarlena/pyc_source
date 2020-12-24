# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/captcha/browser/captcha.py
# Compiled at: 2014-10-14 10:09:18
__docformat__ = 'restructuredtext'
from cStringIO import StringIO
from ztfy.captcha.api import getCaptcha

class CaptchaView(object):
    """Generate and returns a captcha image"""

    def getCaptcha(self):
        _text, img = getCaptcha(id=self.request.form.get('id'), length=6, request=self.request)
        data = StringIO()
        img.save(data, 'JPEG')
        img_data = data.getvalue()
        if self.request is not None:
            self.request.response.setHeader('Content-Type', 'image/jpeg')
            self.request.response.setHeader('Content-Length', len(img_data))
            self.request.response.setHeader('Cache-Control', 'private,no-cache,no-store')
        return img_data
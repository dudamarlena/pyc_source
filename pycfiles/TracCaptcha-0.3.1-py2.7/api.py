# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/trac_captcha/api.py
# Compiled at: 2011-02-03 12:14:17
from trac.core import Interface
__all__ = [
 'CaptchaFailedError', 'ICaptcha']

class CaptchaFailedError(Exception):

    def __init__(self, msg, captcha_data=None):
        Exception.__init__(self, msg)
        self.msg = msg
        self.captcha_data = captcha_data or dict()


class ICaptcha(Interface):
    """Extension point interface for components that implement a specific 
    captcha."""

    def genshi_stream(self):
        """Return a Genshi stream which contains the captcha implementation."""
        pass

    def assert_captcha_completed(self, req):
        """Check the request if the captcha was completed successfully. If the
        captcha is incomplete, a CaptchaFailedError is raised."""
        pass
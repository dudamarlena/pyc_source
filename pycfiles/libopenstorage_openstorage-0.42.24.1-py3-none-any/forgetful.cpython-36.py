# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/requests-toolbelt/requests_toolbelt/cookies/forgetful.py
# Compiled at: 2020-01-10 16:25:32
# Size of source mod 2**32: 213 bytes
"""The module containing the code for ForgetfulCookieJar."""
from requests.cookies import RequestsCookieJar

class ForgetfulCookieJar(RequestsCookieJar):

    def set_cookie(self, *args, **kwargs):
        pass
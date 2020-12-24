# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/alman/apibits/headers_builder.py
# Compiled at: 2015-08-31 22:18:13
import alman
from .errors import AuthenticationError
import base64, json, platform

class HeadersBuilder(object):

    @classmethod
    def default_headers(cls):
        user_agent = {'bindings_version': '0.0.1', 
           'lang': 'python', 
           'publisher': 'paid', 
           'httplib': 'requests'}
        for attr, func in [['lang_version', platform.python_version],
         [
          'platform', platform.platform],
         [
          'uname', lambda : (' ').join(platform.uname())]]:
            try:
                val = func()
            except Exception as e:
                val = '!! %s' % (e,)

            user_agent[attr] = val

        headers = {'X-Paid-Client-User-Agent': json.dumps(user_agent), 
           'User-Agent': 'Alman/v1 PythonBindings/%s' % ('0.0.1', ), 
           'Alman-Version': 'v0'}
        return headers

    @classmethod
    def build(cls, dev_headers):
        headers = cls.default_headers()
        headers.update(dev_headers)
        return headers
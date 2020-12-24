# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/extras/cookies/get_cookies.py
# Compiled at: 2016-11-15 17:03:38
# Size of source mod 2**32: 949 bytes
from six import string_types
from dyson.errors import DysonError
from dyson.utils.module import DysonModule

class GetCookiesModule(DysonModule):

    def run(self, webdriver, params):
        """
        Get specific cookies, or all cookies.
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, dict):
            if 'name' in params:
                return webdriver.get_cookie(params['name'])
        else:
            if isinstance(params, list):
                cookies = list()
                for cookie in params:
                    cookies.append(webdriver.get_cookie(cookie))

                return cookies
            if isinstance(params, string_types):
                if params is 'all':
                    return webdriver.get_cookies()
                raise DysonError('Don\'t know how to fetch "%s". To get all cookies, specify "all"')
            else:
                raise DysonError('Invalid type')
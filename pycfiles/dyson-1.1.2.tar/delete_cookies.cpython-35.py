# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/extras/cookies/delete_cookies.py
# Compiled at: 2016-11-15 16:46:26
# Size of source mod 2**32: 609 bytes
from six import string_types
from dyson.utils.module import DysonModule

class DeleteCookiesModule(DysonModule):

    def run(self, webdriver, params):
        """
        Delete specific cookies, or delete all cookies
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, list):
            for cookie in params:
                webdriver.delete_cookie(cookie)

        else:
            if isinstance(params, string_types):
                if params is 'all':
                    webdriver.delete_all_cookies()
            else:
                webdriver.delete_cookie(params)
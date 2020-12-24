# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/extras/cookies/add_cookies.py
# Compiled at: 2016-11-15 17:12:04
# Size of source mod 2**32: 469 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule

class AddCookiesModule(DysonModule):

    def run(self, webdriver, params):
        """
        Add cookie(s) to the session
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, list):
            for cookie in params:
                webdriver.add_cookie(cookie)

        else:
            raise DysonError('Type needs to be array.')
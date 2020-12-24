# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/navigation/navigate.py
# Compiled at: 2016-11-15 02:21:08
# Size of source mod 2**32: 745 bytes
from six import string_types
from dyson.errors import DysonError
from dyson.modules.core.navigation.goto import GotoModule
from dyson.utils.module import DysonModule

class NavigateModule(DysonModule):

    def run(self, webdriver, params):
        """
        Navigate between pages.
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, string_types):
            if 'forward' is params:
                webdriver.forward()
            elif 'back' is params:
                webdriver.back()
        else:
            if isinstance(params, dict):
                if 'to' in params:
                    GotoModule().run(webdriver, {'url': params['to']})
            else:
                raise DysonError('Invalid type')
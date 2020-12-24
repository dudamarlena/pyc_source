# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/windows/get_window_handles.py
# Compiled at: 2016-11-15 02:36:21
# Size of source mod 2**32: 300 bytes
from dyson.utils.module import DysonModule

class GetWindowHandlesModule(DysonModule):

    def run(self, webdriver, params):
        """
        Return the available window handles
        :param webdriver:
        :param params:
        :return:
        """
        return webdriver.window_handles
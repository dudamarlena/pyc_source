# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/core/navigation/goto.py
# Compiled at: 2016-11-11 03:47:10
# Size of source mod 2**32: 434 bytes
from dyson.errors import DysonError
from dyson.utils.module import DysonModule

class GotoModule(DysonModule):

    def run(self, webdriver, params):
        if isinstance(params, dict):
            if params['url']:
                return webdriver.get(params['url'])
            raise DysonError('You need to specify a valid URL to go to')
        else:
            raise DysonError('Key "url" is required')
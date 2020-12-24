# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/extras/waits/sleep.py
# Compiled at: 2016-11-15 02:23:05
# Size of source mod 2**32: 1129 bytes
from six import string_types
import time
from dyson.errors import DysonError
from dyson.utils.module import DysonModule

class SleepModule(DysonModule):
    VALID_OPTIONS = frozenset(['seconds', 's', 'milliseconds', 'ms'])

    def run(self, webdriver, params):
        """
        Sleep for a time
        :param webdriver:
        :param params:
        :return:
        """
        if isinstance(params, string_types):
            time.sleep(params)
        else:
            if isinstance(params, dict):
                if 'seconds' in params:
                    time.sleep(params['seconds'])
            else:
                if 's' in params:
                    time.sleep(params['s'])
                else:
                    if 'ms' in params:
                        ms = int(params['ms'])
                        time.sleep(ms / 1000)
                    else:
                        if 'milliseconds' in params:
                            ms = int(params['milliseconds'])
                            time.sleep(ms / 1000)
                        else:
                            raise DysonError('Invalid option "%s" for sleep. Valid options are %s' % (params, ','.join(self.VALID_OPTIONS)))
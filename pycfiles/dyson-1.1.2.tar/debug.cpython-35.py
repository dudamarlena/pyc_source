# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dj/workspace/dyson-py/lib/dyson/modules/extras/debug/debug.py
# Compiled at: 2016-11-12 00:05:31
# Size of source mod 2**32: 410 bytes
from dyson.utils.module import DysonModule

class DebugModule(DysonModule):

    def run(self, webdriver, params):
        try:
            if 'var' in params:
                print('DEBUG: %s' % params['var'])
                return params['var']
            if 'msg' in params:
                print('DEBUG: %s' % params['msg'])
                return params['var']
        except:
            print(params)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/virtualenv/python3.5.3/lib/python3.5/site-packages/py_type/output.py
# Compiled at: 2017-11-12 22:10:17
# Size of source mod 2**32: 693 bytes


class Output:

    def __init__(self):
        pass

    debug = False
    check_enabled = True
    check_level = 'all'
    levels = {'all': 1, 
     'trace': 2, 
     'debug': 3, 
     'info': 4, 
     'warn': 5, 
     'error': 6, 
     'fatal': 7, 
     'off': 8}

    @staticmethod
    def error_func(s):
        raise Exception(s)

    def do_check(self, level):
        if self.debug:
            print('check-enabled: ' + str(self.check_enabled) + ', level: ' + level + ', check-level: ' + self.check_level)
        return self.check_enabled & (self.levels[self.check_level] <= self.levels[level])


output = Output()
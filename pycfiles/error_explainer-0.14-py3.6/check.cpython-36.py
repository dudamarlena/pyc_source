# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/error_explainer/check.py
# Compiled at: 2020-04-27 11:40:35
# Size of source mod 2**32: 256 bytes


class Check:
    __doc__ = '\n    Wrapper class for holding the level and function of a check.\n    '

    def __init__(self, level, function):
        self.level = level
        self.function = function

    def run(self, *kwargs):
        (self.function)(*kwargs)
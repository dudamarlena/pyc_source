# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/controller/exceptions.py
# Compiled at: 2015-06-17 12:23:17
# Size of source mod 2**32: 398 bytes


class QuitController(Exception):
    __doc__ = '\n    Immediately ends controller. Controller will return provided response.\n    '

    def __init__(self, response=None):
        self.response = response


class FinalizeController(Exception):
    __doc__ = '\n    Ends .make method. Other Controller mechanics will work normally.\n    '

    def __init__(self, context=None):
        self.context = context or {}
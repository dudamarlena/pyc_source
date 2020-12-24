# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/formskit/errors.py
# Compiled at: 2015-07-25 09:04:48
# Size of source mod 2**32: 273 bytes


class BadValue(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class ValueNotPresent(Exception):

    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name
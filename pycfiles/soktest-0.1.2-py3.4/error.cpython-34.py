# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soktest/error.py
# Compiled at: 2013-11-08 09:04:33
# Size of source mod 2**32: 92 bytes


class NameAlreadyExists(Exception):

    def __init__(self, name):
        self.name = name
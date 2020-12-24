# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/ffexception.py
# Compiled at: 2012-09-21 06:57:35


class FFException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
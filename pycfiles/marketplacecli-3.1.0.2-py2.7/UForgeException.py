# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/marketplacecli/exceptions/UForgeException.py
# Compiled at: 2016-06-03 07:47:35
__author__ = 'UShareSoft'

class UForgeException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
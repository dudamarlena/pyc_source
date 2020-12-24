# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/asterisk_dialplan/dialplan_exceptions.py
# Compiled at: 2015-03-13 22:04:52
""" Exception classes for asterisk_dialplan """

class DialplanException(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)
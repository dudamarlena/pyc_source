# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nino/dev/marx/tests/workflow/example_objects.py
# Compiled at: 2014-09-26 20:08:33
"""
Created on Mar 2, 2013

@author: nino
"""

class PermissionDeniedError(Exception):
    pass


class User(object):

    def __init__(self, name):
        self.name = name

    def is_authorized(self, action):
        return True

    def can_throw(self):
        return False

    def increment(self, stat, count=1):
        pass
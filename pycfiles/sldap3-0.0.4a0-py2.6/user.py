# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\sldap3\core\user.py
# Compiled at: 2015-03-19 16:44:39
"""
"""

class User(object):

    def __init__(self, identity, authorization=None):
        self.identity = identity
        self.authorization = authorization
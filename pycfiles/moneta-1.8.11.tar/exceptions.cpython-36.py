# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/flanker/Developer/Github/Moneta/moneta/exceptions.py
# Compiled at: 2017-07-10 01:59:22
# Size of source mod 2**32: 226 bytes
__author__ = 'flanker'

class InvalidRepositoryException(BaseException):

    def __init__(self, msg):
        self.msg = msg

    def __unicode__(self):
        return self.msg

    def __str__(self):
        return self.msg
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/exceptions.py
# Compiled at: 2014-11-26 20:36:22
# Size of source mod 2**32: 269 bytes
__author__ = 'rfeather'

class ParsimonyException(Exception):
    __doc__ = ' Base exception for parsimony.\n\n    Extend this for defining exceptions.\n    '

    def __init__(self, message):
        self.message = message

    def ___str__(self):
        return self.message
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/taurusexception.py
# Compiled at: 2019-08-19 15:09:29
"""This module contains the taurus base exception classes"""
__all__ = [
 'TaurusException', 'DoubleRegistration']
__docformat__ = 'restructuredtext'

class TaurusException(Exception):

    def __init__(self, description, code=None):
        self.code = code
        self.description = description

    def __str__(self):
        return str(self.description)


class DoubleRegistration(TaurusException):
    pass
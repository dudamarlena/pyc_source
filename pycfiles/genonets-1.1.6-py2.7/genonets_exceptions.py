# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/genonets/genonets_exceptions.py
# Compiled at: 2017-01-31 16:34:36
"""
    genonets_exceptions
    ~~~~~~~~~~~~~~~~~~~

    Defines custom exceptions.

    :author: Fahad Khalid
    :license: MIT, see LICENSE for more details.
"""

class GenonetsError(Exception):

    def __init__(self, errId, info=''):
        self.errId = errId
        self.info = info

    def __str__(self):
        return repr(self.errId)
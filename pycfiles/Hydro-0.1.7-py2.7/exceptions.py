# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/hydro/exceptions.py
# Compiled at: 2014-11-23 10:45:29
__author__ = 'moshebasanchig'

class HydroException(Exception):

    def __init__(self, message, errors=None):
        Exception.__init__(self, message)
        self.errors = errors
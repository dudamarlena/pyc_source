# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/tests/connection_check_c.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Nov 6, 2012

@author: Nicklas Boerjesson
"""
from ube.concerns.connection import connection_c

@connection_c
class connection_check_class(object):
    _dal = None

    def connection_check(self, _sql):
        self._dal.execute(_sql)
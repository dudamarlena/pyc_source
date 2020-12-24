# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ube/concerns/permission.py
# Compiled at: 2013-09-01 17:36:06
"""
Created on Sep 6, 2012

@author: Nicklas Börjesson
"""
from ube.concerns.connection import connection

class permissions(object):
    """This decorator checks and manages permissions. (Unfinished)"""

    def __init__(self, params):
        """
        Constructor
        """
        pass

    @connection
    def check_object(self, _entityid, _sessionid, _typeguid, _connection=None):
        pass
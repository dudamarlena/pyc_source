# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/checkpermission/interfaces.py
# Compiled at: 2009-11-06 11:57:19
from zope.interface import Interface

class ICheckPermission(Interface):
    """ 
    Check if permissions are ok.
    This is called from the check permission decorator. 
    """
    __module__ = __name__

    def check(permission):
        """ True if you have the rights to do something, otherwise raises Unauthorized """
        pass
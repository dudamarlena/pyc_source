# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/security/tal/interfaces.py
# Compiled at: 2012-06-20 11:58:16
__docformat__ = 'restructuredtext'
from zope.interface import Interface

class ISecurityPermissionTalesAPI(Interface):
    """Security TAL namespace adapter"""

    def __getattr__(permission):
        """Check if given permission if granted on adapted context"""
        pass
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rcom/pas/gapps/interface.py
# Compiled at: 2008-07-07 15:55:22
from Products.PluggableAuthService import interfaces

class IGappsHelper(interfaces.plugins.IAuthenticationPlugin):
    """interface for GappsHelper.

    """
    __module__ = __name__
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/simplon/plone/ldap/ploneldap/interfaces.py
# Compiled at: 2007-11-14 08:14:44
from zope.interface import Interface

class IManagedLDAPPlugin(Interface):
    """Marker interface for the LDAP PAS plugin which is managed by us.
    """
    __module__ = __name__
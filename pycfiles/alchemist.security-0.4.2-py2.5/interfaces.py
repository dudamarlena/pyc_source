# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/alchemist/security/interfaces.py
# Compiled at: 2008-09-11 08:15:48
"""
$Id: $
"""
from zope import interface

class IAlchemistUser(interface.Interface):
    """ the domain class for authentication """

    def checkPassword(password):
        """
        return true if the password matches
        """
        pass


class IAlchemistAuth(interface.Interface):
    """ marker interface on alchemist security components
    for adaptation."""
    pass


class ISecurityLocalPrincipalRoleMap(interface.Interface):
    """
    marker interface for alchemist objects that want to provide
    a local security context
    """
    pass


class ISecurityLocalRolePermissionMap(interface.Interface):
    """
    marker interface for alchemist objects that want to provide
    a local security context
    """
    pass
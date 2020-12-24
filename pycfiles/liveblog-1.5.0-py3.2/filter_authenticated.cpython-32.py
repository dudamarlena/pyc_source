# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/impl/filter_authenticated.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Jan 12, 2013

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

The implementation for the authenticated security filter user service.
"""
from ally.container.support import setup
from superdesk.security.api.filter_authenticated import IAuthenticatedFilterService

@setup(IAuthenticatedFilterService, name='authenticatedFilterService')
class AuthenticatedFilterService(IAuthenticatedFilterService):
    """
    Provides the service that checks if the authenticated identifier is same with the resource identifier.
    """

    def isAllowed(self, authenticated, resourceIdentifier):
        """
        @see: IAuthenticatedFilterService.isAllowed
        """
        return authenticated == resourceIdentifier
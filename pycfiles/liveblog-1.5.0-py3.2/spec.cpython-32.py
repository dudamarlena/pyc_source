# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/superdesk/security/core/spec.py
# Compiled at: 2013-10-02 09:54:57
"""
Created on Sep 9, 2012

@package: superdesk security
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Provides the specification classes for authentication.
"""
import abc

class ICleanupService(metaclass=abc.ABCMeta):
    """
    Specification for cleanup service for authentications/sessions.
    """

    @abc.abstractclassmethod
    def cleanExpired(self):
        """
        Clean the expired authentications/sessions.
        """
        pass


class IUserRbacSupport(metaclass=abc.ABCMeta):
    """
    Provides the user rbac support. 
    """

    @abc.abstractclassmethod
    def rbacIdFor(self, userId):
        """
        Provides the rbac id of the user id.
        
        @param userId: integer
            The user id to provide the rbac id for.
        @return: integer|None
            The rbac id, or None if not available.
        """
        pass
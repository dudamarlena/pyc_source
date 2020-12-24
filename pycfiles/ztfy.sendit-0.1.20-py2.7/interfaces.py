# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/sendit/skin/app/xmlrpc/interfaces.py
# Compiled at: 2013-05-31 13:02:11
from zope.interface import Interface

class ISenditApplicationServices(Interface):
    """Sendit application XML-RPC services definition"""

    def searchPrincipals(self, query, names=None):
        """Search principals matching given query"""
        pass

    def getPrincipalInfo(self, principal_id):
        """Get user profile info"""
        pass

    def canRegisterPrincipal(self):
        """Check if external users registration is opened"""
        pass

    def registerPrincipal(self, email, firstname, lastname, company_name=None):
        """Create a new profile with given attributes"""
        pass

    def uploadPacket(self, title, description, recipients, notification_mode, backup_time, documents):
        """Send a new packet with given properties"""
        pass
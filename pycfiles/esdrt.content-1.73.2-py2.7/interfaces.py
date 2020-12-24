# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/utilities/interfaces.py
# Compiled at: 2019-05-21 05:08:43
from zope.interface import Interface
from zope.interface import Attribute

class ILDAPQuery(Interface):
    """ Query LDAP directly. Using the configuration of the
        provided LDAPUserFolder.
    """
    acl = Attribute("The LDAPUserFolder we're operating on.")
    config = Attribute('Automatically set, after calling connect().')
    connection = Attribute('Automatically set, after calling connect().')

    def connect(acl):
        """ Start LDAP connection. Sets and returns a connection."""
        pass

    def query_ou(ou, query, attrs):
        """ Queries ou for query, requesting attrs.
            Uses the connection initialized by connect().
        """
        pass

    def query_groups(query, attrs):
        """ Helper method, calls query_ou() with self.config['ou_groups'].
        """
        pass

    def query_users(query, attrs):
        """ Helper method, calls query_ou() with self.config['ou_users'].
        """
        pass


class ISetupReviewFolderRoles(Interface):
    """ Grant local, Zope roles to certain LDAP groups.
    """
    pass
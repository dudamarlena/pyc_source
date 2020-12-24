# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/iccommunity/mediawiki/interfaces.py
# Compiled at: 2008-10-06 10:31:13
"""Interfaces
"""
from zope import schema
from zope.interface import Interface
from iccommunity.mediawiki import MediawikiMessageFactory as _

class IRolesPair(Interface):
    """A pair of roles, one from Plone and another from Mediawiki"""
    __module__ = __name__
    plone_role = schema.TextLine(title=_('Plone Role'))
    mediawiki_role = schema.TextLine(title=_('Mediawiki Role'))


class IicCommunityManagementMediawikiRolesMapper(Interface):
    """An interface for a role mapper between Plone and Mediawiki"""
    __module__ = __name__
    rolemap = schema.List(title=_('Roles Map'), required=False, default=[], description=_("Enter a role association per line using the format 'Plone Role, Mediawiki Role' without quotes."), value_type=schema.TextLine(title=_('Map'), required=False))

    def get_parsed_rolemap():
        """Returns a list of pairs containing a string for the Plone
        role and a string for the Mediawiki role.
        """
        pass


class IicCommunityManagementMediawikiSQLServer(Interface):
    """An interface for Mediawiki SQL server configuration"""
    __module__ = __name__
    hostname = schema.DottedName(title=_('Host name'), description=_('The database host name'), default='localhost', required=True)
    username = schema.ASCIILine(title=_('User name'), description=_('The database user name'), default='wikiuser', required=True)
    password = schema.Password(title=_('Password'), description=_('The database password'), required=True)
    database = schema.ASCIILine(title=_('Database name'), description=_('The database name'), default='wikidb', required=True)
    dbprefix = schema.ASCIILine(title=_('Names prefix'), description=_('The prefix of table names'), default='', required=False)
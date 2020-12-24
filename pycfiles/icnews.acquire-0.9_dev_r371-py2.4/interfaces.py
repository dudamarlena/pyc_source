# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/acquire/interfaces.py
# Compiled at: 2008-10-06 10:31:17
"""Package interfaces
"""
from zope.interface import Interface
from zope import schema
from icnews.acquire import ICNewsAquireMessageFactory as _

class IAdqnews(Interface):
    """Acquire news content type"""
    __module__ = __name__
    title = schema.TextLine(title=_('Title'), required=True)
    description = schema.Text(title=_('Description'), required=True)
    source = schema.URI(title=_('Source'), required=True)
    re = schema.Text(title=_('Regular Expresion'))
    encoding = schema.BytesLine(title=_('Encoding'))
    store = schema.Bool(title=_('Store in relational database?'))


class IAdqnewsDB(Interface):
    """Handle the DB aspect of Adqnews"""
    __module__ = __name__

    def store():
        """Store the news items in the DB"""
        pass

    def retrieve(date):
        """Retrieve news items from the DB matcing a specific date"""
        pass


class INewsFromURL(Interface):
    """Get news from URL"""
    __module__ = __name__


class IicNewsManagementAcquireSQLServer(Interface):
    """An interface for the SQL server configuration"""
    __module__ = __name__
    hostname = schema.DottedName(title=_('Host name'), description=_('The database host name'), default='localhost', required=True)
    username = schema.ASCIILine(title=_('User name'), description=_('The database user name'), default='', required=True)
    password = schema.Password(title=_('Password'), description=_('The database password'), required=True)
    database = schema.ASCIILine(title=_('Database name'), description=_('The database name'), default='', required=True)
    dbprefix = schema.ASCIILine(title=_('Names prefix'), description=_('The prefix of table names'), default='', required=False)
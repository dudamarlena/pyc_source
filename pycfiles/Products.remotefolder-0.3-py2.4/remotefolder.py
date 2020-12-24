# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/Products/remotefolder/interfaces/remotefolder.py
# Compiled at: 2010-05-20 08:46:21
from zope import schema
from zope.interface import Interface
from zope.app.container.constraints import contains
from zope.app.container.constraints import containers
from Products.remotefolder import remotefolderMessageFactory as _

class IRemoteFolder(Interface):
    """Folderish type that loads content from an external source like, for example, RSS feeds"""
    __module__ = __name__


class IRemoteDataUpdater(Interface):
    """Class used to convert RSS data into Plone objects."""
    __module__ = __name__

    def getRemoteData(self, remoteFolder):
        """Get items from RSS feed and convert them to plone objects.
        Receives a RemoteFolder item and updates all the URI"""
        pass

    def _getFeed(self, url):
        """ Gets the RSS from the URL and updates it if it already exists"""
        pass

    def _addPloneObjects(self, feed):
        """From a feed object, create plone content in the remote folder"""
        pass
# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/browser/interfaces.py
# Compiled at: 2011-05-20 07:51:00
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope.interface import implements, Interface

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """


class IHeadManager(IViewletManager):
    """Viewlet manager on top of the site to contain the logo and searchbox
    """


class IFooterManager(IViewletManager):
    """Viewlet manager on bottom of the site to contain the login menu
    """


class ISlider(Interface):
    """Viewlet manager on bottom of the site to contain the login menu
    """


class ISearchView(Interface):
    """Used to provide python functions to the search results
    """

    def isVideo(self, item):
        """Tests if the item is a video
        """
        pass

    def audioOnly(self, item):
        """Test if is audio_only
        """
        pass

    def getSearchableTypes(self):
        """Organizes search tab types
        """
        pass

    def getTypeName(self, type):
        """Get the display name (plural) of the type
        """
        pass

    def purgeType(self, type):
        """ Converts to plone types ex: Media to Image and File
        """
        pass

    def createSearchURL(self, request, type):
        """Creates a search URL for the type
        """
        pass
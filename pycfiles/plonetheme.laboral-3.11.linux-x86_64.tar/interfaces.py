# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /var/plone4_dev/Python-2.6/lib/python2.6/site-packages/plonetheme/laboral/browser/interfaces.py
# Compiled at: 2011-05-20 07:51:00
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope.interface import implements, Interface

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
    """
    pass


class IHeadManager(IViewletManager):
    """Viewlet manager on top of the site to contain the logo and searchbox
    """
    pass


class IFooterManager(IViewletManager):
    """Viewlet manager on bottom of the site to contain the login menu
    """
    pass


class ISlider(Interface):
    """Viewlet manager on bottom of the site to contain the login menu
    """
    pass


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
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/plonetheme/colorcontext/browser/interfaces.py
# Compiled at: 2010-09-15 08:23:40
from plone.theme.interfaces import IDefaultPloneLayer
from zope.viewlet.interfaces import IViewletManager
from zope.interface import Interface

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
       If you need to register a viewlet only for the
       "Color Context Theme" theme, this interface must be its layer
       (in colorcontext/viewlets/configure.zcml).
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


class ICSSClassProvider(Interface):
    """Class used to generate css class names to create the color context
    """

    def getColorClass(self, url):
        """Creates a classname to the url of the item passed
        """
        pass
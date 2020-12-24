# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/browser/homepage.py
# Compiled at: 2011-12-07 11:27:07
from zope.interface import implements
from Acquisition import aq_inner
from Products.CMFCore.utils import getToolByName
from Products.Five import BrowserView
from Products.ATContentTypes.interface.folder import IATFolder
from semicinternet.theme.cambrils.browser.interfaces import IHomepage
from zope.component import getUtility
from plone.registry.interfaces import IRegistry
from semicinternet.theme.cambrils.browser.interfaces import ICambrilsSettings
from plone.registry.fieldfactory import persistentFieldAdapter
DEFAULT_NUMBER_OF_ITEMS = 10
DEFAULT_BASE_PATH = ''

class Homepage(BrowserView):
    implements(IHomepage)

    def __init__(self, context, request):
        super(Homepage, self).__init__(context, request)
        self.portal = getToolByName(self.context, 'portal_url').getPortalObject()

    def getDropDownMenuLevels(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        try:
            level = settings.dropdown_menu_levela
        except AttributeError:
            level = 0

        return level

    def getDropdownMenu(self, actual_base_path=DEFAULT_BASE_PATH):
        urltool = getToolByName(self, 'portal_url')
        catalog = getToolByName(self, 'portal_catalog')
        if len(actual_base_path) > 0:
            site_root = actual_base_path
        else:
            site_root = urltool.getPortalPath()
        newList = []
        query_result = catalog({'Type': {'query': ['Folder', 'ATFolder', 'Page', 'ATPage']}, 'path': {'query': site_root, 'level': 0, 'depth': 1}, 'sort_on': 'getObjPositionInParent'})
        for brain in query_result:
            if brain.getObject()['excludeFromNav'] == False:
                newList.append(brain)

        if query_result:
            return newList
        else:
            return False

    def getSlideshowImages(self, num_items=DEFAULT_NUMBER_OF_ITEMS):
        urltool = getToolByName(self, 'portal_url')
        catalog = getToolByName(self, 'portal_catalog')
        section_path = ('/').join([ str(x) for x in self.context.getPhysicalPath() ]) + '/' + self.getSlideshowFolder()
        query_result = catalog({'Type': {'query': ['Image', 'ATImage']}, 'path': {'query': section_path, 'level': 0}})[:num_items]
        if query_result:
            return [ brain.getObject() for brain in query_result ]
        else:
            section_path = urltool.getPortalPath() + '/' + self.getSlideshowFolder()
            query_result = catalog({'Type': {'query': ['Image', 'ATImage']}, 'path': {'query': section_path, 'level': 0}})[:num_items]
            if query_result:
                return [ brain.getObject() for brain in query_result ]
            return False

    def getSlideshowImageItems(self):
        urltool = getToolByName(self, 'portal_url')
        catalog = getToolByName(self, 'portal_catalog')
        section_path = ('/').join([ str(x) for x in self.context.getPhysicalPath() ]) + '/' + self.getSlideshowFolder()
        query_result = catalog({'Type': {'query': ['Image', 'ATImage']}, 'path': {'query': section_path, 'level': 0}})
        if query_result:
            return len(query_result)
        else:
            section_path = urltool.getPortalPath() + '/' + self.getSlideshowFolder()
            query_result = catalog({'Type': {'query': ['Image', 'ATImage']}, 'path': {'query': section_path, 'level': 0}})
            if query_result:
                return len(query_result)
            return False

    def getSlideshowFolder(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.slideshow_folder

    def getCompanyName(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.company_name

    def getCompanyAboutLine1(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.company_about_line1

    def getCompanyAboutLine2(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.company_about_line2

    def getCompanyAboutLine3(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.company_about_line3

    def getCompanyAboutLine4(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.company_about_line4

    def getAuthorName(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.author_name

    def getAuthorUrl(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.author_url

    def showSocialIcons(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        if settings.facebook_fanpage or settings.flickr_page or settings.twitter_stream or settings.youtube_channel:
            return True
        else:
            return False

    def getFacebookFanpage(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.facebook_fanpage

    def getFlickrPage(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.flickr_page

    def getTwitterStream(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.twitter_stream

    def getYoutubeChannel(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ICambrilsSettings)
        return settings.youtube_channel
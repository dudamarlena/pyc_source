# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/semicinternet/theme/cambrils/browser/interfaces.py
# Compiled at: 2011-09-16 06:27:06
from z3c.form import interfaces
from z3c.form.browser import checkbox
from zope import schema
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory
from semicinternet.theme.cambrils import cambrilsMessageFactory as _
from plone.app.vocabularies.catalog import SearchableTextSourceBinder
from plone.portlets.interfaces import IPortletDataProvider
from plone.theme.interfaces import IDefaultPloneLayer

class IThemeSpecific(IDefaultPloneLayer):
    """Marker interface that defines a Zope 3 browser layer.
           If you need to register a viewlet only for the
           "SEMIC Internet Cambrils Theme" theme, this interface must be its layer
           (in theme/cambrils/viewlets/configure.zcml).
        """
    pass


class IGalleryPortlet(IPortletDataProvider):
    image_count = schema.Int(title=_('Number of images to display'), description=_('How many images to list.'), required=True, default=5)
    image_root_folder = schema.Choice(title=_('label_navigation_root_path', default='Root node for image gallery'), description=_('help_navigation_root', default='You may search for and choose a folder to act as the root of the image gallery.Leave blank to use the Plone site root.'), required=False, source=SearchableTextSourceBinder({'is_folderish': True}, default_query='path:'))
    path_depth = schema.Int(title=_('Path depth'), description=_('How many depth to search inside the root folder.'), required=True, default=1)


class IHomepage(Interface):
    """Browser view for homepage logic"""

    def getDropDownMenuLevels():
        """Returns the number of levels to show in the dropbox menu
                """
        pass

    def getDropdownMenu():
        """Returns the number of images inside the slideshow folder
                """
        pass

    def getSlideshowImages():
        """Returns the number of images inside the slideshow folder
                """
        pass

    def getSlideshowFolder():
        """Returns the id of the folder containing the slide images.
                """
        pass

    def getCompanyName():
        """Returns a string containing the company name, this is part of the copyright shown at the bottom right part.
                """
        pass

    def getCompanyAboutLine1():
        """Returns a string containing an optional line to be shown at the bottom right part (address, etc...)
                """
        pass

    def getCompanyAboutLine2():
        """Returns a string containing an optional line to be shown at the bottom right part (address, etc...)
                """
        pass

    def getCompanyAboutLine3():
        """Returns a string containing an optional line to be shown at the bottom right part (address, etc...)
                """
        pass

    def getCompanyAboutLine4():
        """Returns a string containing an optional line to be shown at the bottom right part (address, etc...)
                """
        pass

    def getAuthorName():
        """Returns a string containing the website author name to be shown at the bottom left part.
                """
        pass

    def getAuthorUrl():
        """Returns a string containing the url address of the author's website.
                """
        pass

    def showSocialIcons():
        """Returns True if any social URL is set
                """
        pass

    def getFacebookFanpage():
        """Returns a string containing the url of the facebook fan page
                """
        pass

    def getFlickrPage():
        """Returns a string containing the url of the flickr page
                """
        pass

    def getTwitterStream():
        """Returns a string containing the url of the twitter stream page
                """
        pass

    def getYoutubeChannel():
        """Returns a string containing the url of the youtube channel page
                """
        pass


class ICambrilsSettings(Interface):
    """Global cambrils settings. This describes records stored in the configuration 
           registry and otainable via plone.registry."""
    dropdown_menu_level = schema.Choice(title=_('Number of levels in dropdown menu'), description=_('help_dropdown_menu_levels', default='Select the number of levels, 0 to disable the dropdown effect'), required=True, values=[
     '0', '1', '2'])
    slideshow_folder = schema.TextLine(title=_('Slideshow folder'), description=_('help_slideshow_folder', default='Name of the folder containing the slideshow images.'), required=True, default='slideshow')
    company_name = schema.TextLine(title=_('Company name'), description=_('help_company_name', default='Name of the website owner.'), required=False, default='Company name')
    company_about_line1 = schema.TextLine(title=_('Company about line 1'), description=_('help_company_about_line1', default='Address or other information (line 1).'), required=False, default='Company about line 1')
    company_about_line2 = schema.TextLine(title=_('Company about line 2'), description=_('help_company_about_line2', default='Address or other information (line 2).'), required=False, default='Company about line 2')
    company_about_line3 = schema.TextLine(title=_('Company about line 3'), description=_('help_company_about_line3', default='Address or other information (line 3).'), required=False, default='Company about line 3')
    company_about_line4 = schema.TextLine(title=_('Company about line 4'), description=_('help_company_about_line4', default='Address or other information (line 4).'), required=False, default='Company about line 4')
    author_name = schema.TextLine(title=_('Website author name'), description=_('help_author_name', default='Name of your company, or website creator.'), required=False, default='SEMIC Internet')
    author_url = schema.TextLine(title=_('Website author URL'), description=_('help_author_url', default='Website URL of your company or website creator.'), required=False, default='http://www.semicinternet.com')
    facebook_fanpage = schema.TextLine(title=_('Facebook Fanpage URL'), description=_('help_facebook_fanpage', default='The url of your facebook fan page'), required=False, default='')
    flickr_page = schema.TextLine(title=_('Flickr Account URL'), description=_('help_flickr_page', default='The url of your flickr account page'), required=False, default='')
    twitter_stream = schema.TextLine(title=_('Twitter Stream URL'), description=_('help_twitter_stream', default='The url of your twitter stream page.'), required=False, default='')
    youtube_channel = schema.TextLine(title=_('YouTube Channel URL'), description=_('help_youtube_channel', default='The url of your youtube channel page'), required=False, default='')
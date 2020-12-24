# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\fhkrems\portlet\youtubeplayer\youtubeplayerportlet.py
# Compiled at: 2010-07-21 04:48:07
from zope.component import getUtility
from zope.interface import implements
from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets import base
from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from fhkrems.portlet.youtubeplayer import YouTubePlayerPortletMessageFactory as _
from plone.i18n.normalizer.interfaces import IIDNormalizer

class IYouTubePlayerPortlet(IPortletDataProvider):
    """A portlet

    It inherits from IPortletDataProvider because for this portlet, the
    data that is being rendered and the portlet assignment itself are the
    same.
    """
    __module__ = __name__
    header = schema.TextLine(title=_('youtubeplayerportlet_header_label', default='Portlet header'), description=_('youtubeplayerportlet_header_description', default='Title of the rendered portlet'), required=True)
    url = schema.TextLine(title=_('youtubeplayerportlet_url_label', default='YouTube VideoID'), description=_('youtubeplayerportlet_url_description', default='ID of the youtube video'), required=True)
    width = schema.TextLine(title=_('youtubeplayerportlet_width_label', default='Width'), description=_('youtubeplayerportlet_width_description', default='Set width of Player'), required=True)
    height = schema.TextLine(title=_('youtubeplayerportlet_height_label', default='Height'), description=_('youtubeplayerportlet_height_description', default='Set height of Player incl. 25px of controls'), required=True)
    hl = schema.TextLine(title=_('youtubeplayerportlet_hl_label', default='Language'), description=_('youtubeplayerportlet_hl_description', default='For more Information look here: http://code.google.com/apis/youtube/2.0/reference.html#Localized_Category_Lists'), required=True)
    rel = schema.Bool(title=_('youtubeplayerportlet_rel_label', default='Relational Videos'), description=_('youtubeplayerportlet_rel_description', default='Sets whether the player should load related videos once playback of the initial video starts.'), required=False, default=False)
    fs = schema.Bool(title=_('youtubeplayerportlet_fs_label', default='Fullscreen'), description=_('youtubeplayerportlet_fs_description', default='Setting to True enables the fullscreen button.'), required=False, default=True)
    hd = schema.Bool(title=_('youtubeplayerportlet_hd_label', default='Enable HD-Video playback button'), description=_('youtubeplayerportlet_hd_description', default='Enable the HD playback button. This button only has an effect if an HD version of the video os available.'), required=False, default=True)
    autoplay = schema.Bool(title=_('youtubeplayerportlet_autoplay_label', default='Autoplay'), description=_('youtubeplayerportlet_autoplay_description', default='Sets whether or not the initial video will autoplay when the player loads.'), required=False, default=False)
    loop = schema.Bool(title=_('youtubeplayerportlet_loop_label', default='Loop'), description=_('youtubeplayerportlet_loop_description', default='If the player is loading a single video, play the video again and again.'), required=False, default=False)
    disablekb = schema.Bool(title=_('youtubeplayerportlet_disablekb_label', default='Disable Keyboard Controls'), description=_('youtubeplayerportlet_disablekb_description', default='Disable player Keyboard controls'), required=False, default=False)
    showinfo = schema.Bool(title=_('youtubeplayerportlet_showinfo_label', default='Show Information'), description=_('youtubeplayerportlet_showinfo_description', default='Setting to True causes the player to not display information like the video title and rating before the video starts playing.'), required=False, default=True)
    footer = schema.TextLine(title=_('youtubeplayerportlet_footer_label', default='Portlet footer'), description=_('youtubeplayerportlet_footer_description', default='Text to be shown in the footer'), required=False)
    more_url = schema.ASCIILine(title=_('youtubeplayerportlet_moreurl_label', default='Details link'), description=_('youtubeplayerportlet_moreurl_description', default='If given, the header and footer will link to this URL.'), required=False)
    omit_border = schema.Bool(title=_('youtubeplayerportlet_omitborder_label', default='Omit portlet border'), description=_('youtubeplayerportlet_omitborder_description', default='Tick this box if you want to render the text above without the standard header, border or footer.'), required=True, default=False)
    hide = schema.Bool(title=_('youtubeplayerportlet_hide_label', default='Hide portlet'), description=_('youtubeplayerportlet_hide_description', default='Tick this box if you want to temporarily hide the portlet without losing your text.'), required=True, default=False)


class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """
    __module__ = __name__
    implements(IYouTubePlayerPortlet)
    header = _('youtubeplayerportlet_title', default='YouTube Player Portlet')
    footer = ''
    more_url = ''
    url = ''
    hl = ''
    height = ''
    width = ''
    rel = False
    fs = False
    hd = True
    autoplay = False
    loop = False
    disablekb = False
    showinfo = False
    omit_border = False
    hide = False

    def __init__(self, header='', url='', hl='', height='', width='', rel=False, fs=False, hd=True, omit_border=False, autoplay=False, loop=False, disablekb=False, showinfo=False, footer='', more_url='', hide=False):
        self.header = header
        self.url = url
        self.width = width
        self.height = height
        self.hl = hl
        self.rel = rel
        self.fs = fs
        self.hd = hd
        self.autoplay = autoplay
        self.loop = loop
        self.disablekb = disablekb
        self.showinfo = showinfo
        self.footer = footer
        self.more_url = more_url
        self.omit_border = omit_border
        self.hide = hide

    @property
    def title(self):
        """This property is used to give the title of the portlet in the
        "manage portlets" screen.
        """
        return 'YouTube Player Portlet'


class Renderer(base.Renderer):
    """Portlet renderer.

    This is registered in configure.zcml. The referenced page template is
    rendered, and the implicit variable 'view' will refer to an instance
    of this class. Other methods can be added and referenced in the template.
    """
    __module__ = __name__
    render = ViewPageTemplateFile('youtubeplayerportlet.pt')

    @property
    def available(self):
        return not self.data.hide

    def css_class(self):
        """Generate a CSS class from the portlet header
        """
        header = self.data.header
        normalizer = getUtility(IIDNormalizer)
        return 'portlet-googlemaps-%s' % normalizer.normalize(header)

    def has_link(self):
        return bool(self.data.more_url)

    def has_footer(self):
        return bool(self.data.footer)


class AddForm(base.AddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    __module__ = __name__
    form_fields = form.Fields(IYouTubePlayerPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(base.EditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    __module__ = __name__
    form_fields = form.Fields(IYouTubePlayerPortlet)
    label = _('title_edit_youtubeplayer_portlet', default='Edit YouTube Player portlet')
    description = _('description_youtubeplayer_portlet', default='A portlet which can display a simple YouTube Player.')
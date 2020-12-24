# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/hvelarde/forcontent/idg/src/brasil.gov.portal/src/brasil/gov/portal/controlpanel/site.py
# Compiled at: 2018-10-18 17:35:13
from brasil.gov.portal import _
from plone import api
from plone.app.controlpanel.form import ControlPanelForm
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import safe_unicode
from zope.component import adapter
from zope.formlib import form
from zope.formlib.textwidgets import TextAreaWidget
from zope.interface import implementer
from zope.interface import Interface
from zope.schema import Bool
from zope.schema import SourceText
from zope.schema import Text
from zope.schema import TextLine

class ISiteSchema(Interface):
    site_title_1 = TextLine(title=_('Site title (First Line)'), description=_('First line of site title'), required=False, default='')
    site_title_2 = TextLine(title=_('Site title (Second Line)'), description=_('Second line of site title'), default='')
    site_orgao = TextLine(title=_('Department'), description=_('Name of Ministry or Department to which this site is subject.'), required=False, default='')
    url_orgao = TextLine(title=_('Url ID of Department'), description=_('Url ID for Ministry or Department to which this site is subject.'), required=False, default='')
    site_description = Text(title=_('Site description'), description=_('The site description is available in syndicated content and in search engines. Keep it brief.'), default='', required=False)
    exposeDCMetaTags = Bool(title=_('Expose Dublin Core metadata'), description=_('Exposes the Dublin Core properties as metatags.'), default=False, required=False)
    display_pub_date_in_byline = Bool(title=_('Display publication date in about information'), description=_('Displays content publication date on site pages.'), default=False, required=False)
    enable_sitemap = Bool(title=_('Expose sitemap.xml.gz'), description=_('Exposes your content as a file according to the sitemaps.org standard. You can submit this to compliant search engines like Google, Yahoo and Microsoft. It allows these search engines to more intelligently crawl your site.'), default=False, required=False)
    webstats_js = SourceText(title=_('JavaScript for web statistics support'), description=_('For enabling web statistics support from external providers (for e.g. Google Analytics). Paste the code snippets provided. It will be included in the rendered HTML as entered near the end of the page.'), default='', required=False)


@implementer(ISiteSchema)
@adapter(IPloneSiteRoot)
class SiteControlPanelAdapter(SchemaAdapterBase):

    def __init__(self, context):
        super(SiteControlPanelAdapter, self).__init__(context)
        self.portal = api.portal.get()
        self.pprop = getToolByName(context, 'portal_properties')
        self.context = self.pprop.site_properties
        self.encoding = self.pprop.site_properties.default_charset

    def get_site_title(self):
        title = getattr(self.portal, 'title', '')
        return safe_unicode(title)

    def set_site_title(self, value):
        pass

    def get_site_title_1(self):
        title = getattr(self.portal, 'title_1', '')
        return safe_unicode(title)

    def set_site_title_1(self, value):
        value = value or ''
        self.portal.title_1 = value.encode(self.encoding)
        title_1 = safe_unicode(self.portal.title_1)
        title_2 = safe_unicode(self.portal.title_2)
        title = '%s %s' % (title_1, title_2)
        self.portal.title = title.encode(self.encoding)

    def get_site_title_2(self):
        title = getattr(self.portal, 'title_2', '')
        return safe_unicode(title)

    def set_site_title_2(self, value):
        value = value or ''
        self.portal.title_2 = value.encode(self.encoding)
        title_1 = safe_unicode(self.portal.title_1)
        title_2 = safe_unicode(self.portal.title_2)
        title = '%s %s' % (title_1, title_2)
        self.portal.title = title.encode(self.encoding)

    def get_site_orgao(self):
        orgao = getattr(self.portal, 'orgao', '')
        return safe_unicode(orgao)

    def set_site_orgao(self, value):
        value = value or ''
        self.portal.orgao = value.encode(self.encoding)

    def get_url_orgao(self):
        configs = getattr(self.pprop, 'brasil_gov', None)
        url_orgao = configs.getProperty('url_orgao', '')
        return safe_unicode(url_orgao)

    def set_url_orgao(self, value):
        value = value or ''
        configs = getattr(self.pprop, 'brasil_gov', None)
        configs.manage_changeProperties(url_orgao=value)
        return

    def get_site_description(self):
        description = getattr(self.portal, 'description', '')
        return safe_unicode(description)

    def set_site_description(self, value):
        if value is not None:
            self.portal.description = value.encode(self.encoding)
        else:
            self.portal.description = ''
        return

    def get_webstats_js(self):
        description = getattr(self.context, 'webstats_js', '')
        return safe_unicode(description)

    def set_webstats_js(self, value):
        if value is not None:
            self.context.webstats_js = value.encode(self.encoding)
        else:
            self.context.webstats_js = ''
        return

    site_title = property(get_site_title, set_site_title)
    site_title_1 = property(get_site_title_1, set_site_title_1)
    site_title_2 = property(get_site_title_2, set_site_title_2)
    site_orgao = property(get_site_orgao, set_site_orgao)
    url_orgao = property(get_url_orgao, set_url_orgao)
    site_description = property(get_site_description, set_site_description)
    webstats_js = property(get_webstats_js, set_webstats_js)
    enable_sitemap = ProxyFieldProperty(ISiteSchema['enable_sitemap'])
    exposeDCMetaTags = ProxyFieldProperty(ISiteSchema['exposeDCMetaTags'])

    def get_display_pub_date_in_byline(self):
        return self.context.site_properties.displayPublicationDateInByline

    def set_display_pub_date_in_byline(self, value):
        self.context.site_properties.displayPublicationDateInByline = value

    display_pub_date_in_byline = property(get_display_pub_date_in_byline, set_display_pub_date_in_byline)


class MiniTextAreaWidget(TextAreaWidget):
    height = 3


class SmallTextAreaWidget(TextAreaWidget):
    height = 5


class SiteControlPanel(ControlPanelForm):
    form_fields = form.FormFields(ISiteSchema)
    form_fields['site_description'].custom_widget = MiniTextAreaWidget
    form_fields['webstats_js'].custom_widget = SmallTextAreaWidget
    label = _('Site settings')
    description = _('Site-wide settings.')
    form_name = _('Site settings')
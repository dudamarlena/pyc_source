# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/browser/controlpanel.py
# Compiled at: 2008-10-10 10:13:59
"""
Sitestat global options control panel
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
import urlparse
from zope.interface import Interface, Attribute
from zope.interface import implements
from zope.component import adapts
from zope.schema import Bool
from zope.schema import Choice
from zope.schema import ASCIILine
from zope.schema import Tuple
from zope.schema import ValidationError
from zope.app.schema.vocabulary import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from plone.fieldsets.fieldsets import FormFieldsets
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getSiteEncoding
from Products.CMFPlone import PloneMessageFactory as p_
from plone.app.controlpanel.form import ControlPanelForm
from iw.sitestat.formlib import URLLine
from iw.sitestat.config import PROPERTYSHEET
from iw.sitestat.utils import getSite, validateSitestatName
from iw.sitestat import IwSitestatMessageFactory as _

class InvalidASCIILabel(ValidationError):
    __module__ = __name__
    __doc__ = _('error_invalid_label', default='Label has unauthorized characters.')


def validateASCIILabel(value):
    if not validateSitestatName(value):
        raise InvalidASCIILabel(value)
    return True


class InvalidURL(ValidationError):
    __module__ = __name__
    __doc__ = _('error_invalid_url', default='Invalid URL form.')


def validateOptionalURL(value):
    if len(value) == 0:
        return True
    parsed = urlparse.urlparse(value)
    if parsed[0] not in ('http', 'https'):
        raise InvalidURL(value)
    unparsed = urlparse.urlunparse(parsed)
    if unparsed != value:
        raise InvalidURL(value)
    return True


class ISitestatGlobalConfigSchema(Interface):
    """Site wide configuration for iw.sitestat"""
    __module__ = __name__
    sitestat_enabled = Bool(title=_('label_sitestat_enabled', default='Enable sitestat?'), description=_('help_sitestat_enabled', default='Will provide your Sitestat service relevant information. <strong>Please check that your Sitestat server is active otherwise this site will unusable</stong>. If unchecked, all options below as well as content local options wil be ignored'), default=False, required=False)
    country_code = Choice(title=_('label_country_code', default='Your country code'), description=_('help_country_code', default='Choose your country in this list'), vocabulary='iw.sitestat.vocabularies.CountryNamesVocabulary', required=True)
    company_code = ASCIILine(title=_('label_company_code', default='Company code'), description=_('help_company_code', default='The company code, as in your Sitestat settings. Only ASCII lowercases.'), required=True, constraint=validateASCIILabel)
    site_code = ASCIILine(title=_('label_site_code', default='Site code'), description=_('help_site_code', default='The site code, as in your Sitestat settings. Only ASCII lowercases.'), required=True, constraint=validateASCIILabel)
    sitestat_private_url = URLLine(title=_('label_sitestat_url', default='Sitestat private URL'), description=_('help_sitestat_url', default='If you have a private Sitestat server, please fill-in its URL.'), required=False)
    counter_name_mode = Choice(title=_('label_counter_name_mode', default='Counter name composition mode'), description=_('help_counter_name_mode', default='Choose what policy we use to build counter names.'), vocabulary='iw.sitestat.vocabularies.CounterNameModeVocabulary', required=True, default='id')
    pdf_marking = Bool(title=_('label_pdf_marking', default='Mark links to PDF files?'), description=_('help_pdf_marking', default='Make special Sitestat URLs to PDF files.'), default=False, required=False)
    files_as_pdf = Bool(title=_('label_files_as_pdf', default='Mark all files links as PDF?'), description=_('help_files_as_pdf', default='Do we mark all links to files (word, excel, ...) as PDF? <strong>This option will be ignored if previous option is unchecked</strong>.'), default=False, required=False)
    dltime_enabled = Bool(title=_('label_dltime_enabled', default='Include page download time'), description=_('help_dltime_enabled', default='Sitestat will have download time information for each page.'), default=False, required=False)
    https_enabled = Bool(title=_('label_https_enabled', default='Enable https://... links on secure pages?'), description=_('help_https_enabled', default='Do <strong>not</strong> check this if your Sitestat settings do not allow https pages, otherwise links from secure pages could be broken.'), default=False, required=False)
    clickin_uids = Attribute('The item UIDs of clickin target')
    clickin_paths = Attribute('The item paths for clickin targets')


class ISitestatClickInOutSchema(Interface):
    """cickin & clickout global config for iw.sitestat"""
    __module__ = __name__
    clickin_enabled = Bool(title=_('label_clickin_enabled', default='Enable clickin?'), description=_('help_clickin_enabled', default='Links to clickin target wil be transformed into Sitestat clickin URLS.'), default=False, required=False)
    clickout_urls = Tuple(title=_('label_clickout_urls', default='Clickout URLs'), description=_('help_clickout_urls', default='URLs of links to other sites to be transformed to Sitestat clickouts.'), value_type=URLLine(), required=False)


class ISitestatConfigSchema(ISitestatGlobalConfigSchema, ISitestatClickInOutSchema):
    """Combined schema"""
    __module__ = __name__


class SitestatControlPanelAdapter(SchemaAdapterBase):
    """Access to iw.sitestat global options
    """
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(ISitestatConfigSchema)

    def __init__(self, context):
        super(SitestatControlPanelAdapter, self).__init__(context)
        self.portal = context
        pprop = getToolByName(self.portal, 'portal_properties')
        self.context = getattr(pprop, PROPERTYSHEET)
        self.encoding = getSiteEncoding(context)

    sitestat_enabled = ProxyFieldProperty(ISitestatConfigSchema['sitestat_enabled'])
    country_code = ProxyFieldProperty(ISitestatConfigSchema['country_code'])
    company_code = ProxyFieldProperty(ISitestatConfigSchema['company_code'])
    site_code = ProxyFieldProperty(ISitestatConfigSchema['site_code'])
    sitestat_private_url = ProxyFieldProperty(ISitestatConfigSchema['sitestat_private_url'])
    counter_name_mode = ProxyFieldProperty(ISitestatConfigSchema['counter_name_mode'])
    pdf_marking = ProxyFieldProperty(ISitestatConfigSchema['pdf_marking'])
    files_as_pdf = ProxyFieldProperty(ISitestatConfigSchema['files_as_pdf'])
    dltime_enabled = ProxyFieldProperty(ISitestatConfigSchema['dltime_enabled'])
    https_enabled = ProxyFieldProperty(ISitestatConfigSchema['https_enabled'])
    clickin_enabled = ProxyFieldProperty(ISitestatConfigSchema['clickin_enabled'])
    clickout_urls = ProxyFieldProperty(ISitestatConfigSchema['clickout_urls'])

    @apply
    def clickin_uids():

        def get(self):
            return self.context.getProperty('clickin_uids')

        def set(self, value):
            self.context.manage_changeProperties(clickin_uids=value)

        return property(get, set)

    @apply
    def clickin_paths():

        def get(self):
            return self.context.getProperty('clickin_paths')

        def set(self, value):
            self.context.manage_changeProperties(clickin_paths=value)

        return property(get, set)


baseset = FormFieldsets(ISitestatGlobalConfigSchema)
baseset.id = 'baseset'
baseset.label = _('label_base_subform', default='Base features')
clickinoutset = FormFieldsets(ISitestatClickInOutSchema)
clickinoutset.id = 'clickinoutset'
clickinoutset.label = _('label_clickinckickout_subform', default='Clickin and Clickout')

class SitestatControlPanel(ControlPanelForm):
    __module__ = __name__
    label = _('label_controlpanel', default='Sitestat settings')
    description = _('help_controlpanel', default='Sitestat site-wide settings.')
    form_name = label
    form_fields = FormFieldsets(baseset, clickinoutset)


class CounterNameModeVocabulary(object):
    """Vocabulary for 'counter_name_mode'. Get it in interface Choice fields
    with the name 'iw.sitestat.vocabularies.CounterNameModeVocabulary' """
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        terms = (
         SimpleTerm('id', 'id', _('obj_identifiers', default='Content identifiers (from URL)')), SimpleTerm('title', 'title', _('obj_titles', default='Content titles')))
        return SimpleVocabulary(terms)


CounterNameModeVocabularyFactory = CounterNameModeVocabulary()

class CountryNamesVocabulary(object):
    """Vocabulary for choosing a country"""
    __module__ = __name__
    implements(IVocabularyFactory)

    def __call__(self, context):
        portal_languages = getToolByName(getSite(), 'portal_languages')
        countries_tuples = [ (x, y['name']) for (x, y) in portal_languages.getAvailableCountries().items() ]
        countries_tuples.sort(lambda x, y: cmp(x[1], y[1]))
        terms = [ SimpleTerm(c[0], c[0], p_(c[1])) for c in countries_tuples ]
        return SimpleVocabulary(terms)


CountryNamesVocabularyFactory = CountryNamesVocabulary()
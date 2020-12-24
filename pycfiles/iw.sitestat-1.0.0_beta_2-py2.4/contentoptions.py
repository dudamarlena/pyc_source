# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/iw/sitestat/browser/contentoptions.py
# Compiled at: 2008-10-10 10:13:59
"""
Content Sitestat options management
"""
__author__ = 'Gilles Lenfant <gilles.lenfant@ingeniweb.com>'
__docformat__ = 'restructuredtext'
from zope.interface import Interface, Attribute
from zope.interface import implements
from zope.component import adapts
from zope.component import getAdapter
from zope.annotation.interfaces import IAnnotations
from zope.schema import Bool, ASCIILine, Tuple
from zope.schema import ValidationError
from zope.app.form.browser.textwidgets import ASCIIWidget
from zope.formlib import form
from Persistence import Persistent
from Products.Five.formlib import formbase
from Products.CMFCore.interfaces import IContentish
from Products.statusmessages.interfaces import IStatusMessage
from Products.CMFPlone import PloneMessageFactory as p_
from iw.sitestat.interfaces import ISitestatConfigSchema
from iw.sitestat.config import ANNOTATIONS_KEY, BLACKLISTED_LABELS
from iw.sitestat.utils import getSite, validateSitestatName
from iw.sitestat import IwSitestatMessageFactory as _
from iw.sitestat import logger

class InvalidCounterError(ValidationError):
    __module__ = __name__
    __doc__ = _('error_invalid_counter', default='This counter is invalid')


def validateCounters(value):
    counters = value.strip().split('.')
    for counter in counters:
        if not bool(counter):
            raise InvalidCounterError
        if not validateSitestatName(counter.lower()):
            raise InvalidCounterError

    return True


class InvalidLabelsError(ValidationError):
    __module__ = __name__
    __doc__ = _('error_invalid_labels', default='One (or more) label is invalid')


class DuplicateLabelError(ValidationError):
    __module__ = __name__
    __doc__ = _('error_duplicate_label', default="Don't duplicate a label name")


class BlacklistedLabelError(ValidationError):
    __module__ = __name__
    __doc__ = _('error_blacklisted_label', default='A label is blacklisted.')


def validateLabels(labels):
    valid_labels = []
    for label_value in labels:
        try:
            (label, value) = [ x.strip() for x in label_value.split('=') ]
        except ValueError, e:
            raise InvalidLabelsError

        if not validateSitestatName(label):
            raise InvalidLabelsError
        if not validateSitestatName(value):
            raise InvalidLabelsError
        if label in valid_labels:
            raise DuplicateLabelError
        if label in BLACKLISTED_LABELS:
            raise BlacklistedLabelError
        valid_labels.append(label)

    return True


class IContentOptions(Interface):
    __module__ = __name__
    is_clickin_target = Bool(title=_('label_is_clickin_target', default='Clickin target?'), description=_('help_is_clickin_target', default="Is this content a clickin target? If checked, all links to this item's view will be transformed into Sitestat clickin URLs."), default=False)
    override_counters = Bool(title=_('label_override_counters', default='Override standard counters'), description=_('help_override_counters', default='Do we override global counter rules for this item?'), default=False)
    counters = ASCIILine(title=_('label_custom_counters', default='Custom counters'), description=_('help_custom_counters', default='Use these counters for this item if you override global counters. Multiple counters must be separated with a dot. Non ASCII characters may not be supported by Sitestat. Example: "Company.Contact".'), constraint=validateCounters, required=False)
    labels = Tuple(title=_('label', default='Labels'), description=_('help_labels', default='Labels for this item. Watch your Sitestat labels list. By default, Sitestat has only the "category" label. Enter label and values in the form "<label>=<value>". Example: "category=sport".'), value_type=ASCIILine(), constraint=validateLabels, required=False)


class OptionsStorage(Persistent):
    """Settings for context local options (stored in context annotations)"""
    __module__ = __name__
    override_counters = False
    counters = ''
    labels = {}


class ContentOptionsManager(object):
    """Adapter for content object that manages local Sitestat options"""
    __module__ = __name__
    adapts(IContentish)
    implements(IContentOptions)

    def __init__(self, context):
        self.context = context
        self.global_config = getAdapter(getSite(), ISitestatConfigSchema)

    @property
    def local_options(self):
        """Proxy to context annotations stored options"""
        annotations = IAnnotations(self.context)
        return annotations.setdefault(ANNOTATIONS_KEY, OptionsStorage())

    @apply
    def is_clickin_target():
        """Proxy on storage, use as a property"""

        def get(self):
            clickin_uids = self.global_config.clickin_uids
            this_uid = self.context.UID()
            return this_uid in clickin_uids

        def set(self, value):
            if get(self) != value:
                clickin_uids = list(self.global_config.clickin_uids)
                if value:
                    clickin_uids.append(self.context.UID())
                else:
                    clickin_uids.remove(self.context.UID())
                self.global_config.clickin_uids = clickin_uids
                compileClickinPaths()

        return property(get, set)

    @apply
    def override_counters():
        """Proxy on storage, use as a property"""

        def get(self):
            return self.local_options.override_counters

        def set(self, value):
            self.local_options.override_counters = bool(value)

        return property(get, set)

    @apply
    def counters():
        """Proxy on storage, use as a property"""

        def get(self):
            return self.local_options.counters

        def set(self, value):
            if value is None:
                value = ''
            self.local_options.counters = value.strip()
            return

        return property(get, set)

    @apply
    def labels():
        """Proxy on storage, use as a property"""

        def get(self):
            labels = self.local_options.labels
            out = [ '%s=%s' % (k, v) for (k, v) in labels.items() ]
            out.sort()
            return tuple(out)

        def set(self, value):
            d_values = {}
            for label in value:
                (k, v) = [ x.strip() for x in label.split('=') ]
                d_values[k] = v

            self.local_options.labels = d_values

        return property(get, set)

    @apply
    def raw_labels():
        """Dict raw value of labels"""

        def get(self):
            return self.local_options.labels

        def set(self, value):
            self.local_options.labels = value

        return property(get, set)


class CountersWidget(ASCIIWidget):
    __module__ = __name__
    displayWidth = 40


class ContentOptionsForm(formbase.EditForm):
    """Our form"""
    __module__ = __name__
    label = _('content_options_title', default='Item specific settings for Sitestat')
    description = _('content_options_help', default='Change or add Sitestat features for this content item.')
    form_fields = form.FormFields(IContentOptions)
    form_fields['counters'].custom_widget = CountersWidget

    @form.action(p_('label_save'))
    def handleApply(self, action, data):
        storage = getAdapter(self.context, IContentOptions)
        is_clickin_target = data['is_clickin_target']
        if storage.is_clickin_target != is_clickin_target:
            global_config = getAdapter(getSite(), ISitestatConfigSchema)
        storage.is_clickin_target = is_clickin_target
        storage.override_counters = data['override_counters']
        storage.counters = data['counters']
        storage.labels = data['labels']
        IStatusMessage(self.request).addStatusMessage(p_('Changes made.'), type='info')
        self.request.RESPONSE.redirect(self.request.URL)
        return ''


def compileClickinPaths():
    portal = getSite()
    global_config = getAdapter(portal, ISitestatConfigSchema)
    catalog = portal.uid_catalog
    paths = []
    for uid in global_config.clickin_uids:
        brains = catalog.searchResults(UID=uid)
        try:
            paths.append(brains[0].getPath())
        except IndexError:
            logger.error('Object with UID %s is gone.', uid)

    global_config.clickin_paths = paths
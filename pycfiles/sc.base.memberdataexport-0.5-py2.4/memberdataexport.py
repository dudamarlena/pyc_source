# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/sc/base/memberdataexport/controlpanel/memberdataexport.py
# Compiled at: 2009-03-29 21:05:56
from zope import schema
from zope.component import adapts
from zope.interface import Interface
from zope.interface import implements
from Products.CMFPlone.interfaces import IPloneSiteRoot
from Products.CMFPlone.utils import getToolByName
from Products.CMFDefault.formlib.schema import ProxyFieldProperty
from Products.CMFDefault.formlib.schema import SchemaAdapterBase
from zope.formlib.form import FormFields
from plone.app.controlpanel.form import ControlPanelForm
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary
from sc.base.memberdataexport import MessageFactory as _
LINETERMINATOR_CHOICES = {_('Windows'): 'win', _('Linux/MacOSX'): 'other'}
LINETERMINATOR_VOCABULARY = SimpleVocabulary([ SimpleTerm(v, v, k) for (k, v) in LINETERMINATOR_CHOICES.items() ])
ENCODING_CHOICES = {_('UTF-8'): 'utf-8', _('ISO-8859-1'): 'iso-8859-1'}
ENCODING_VOCABULARY = SimpleVocabulary([ SimpleTerm(v, v, k) for (k, v) in ENCODING_CHOICES.items() ])

class IExportSchema(Interface):
    __module__ = __name__
    filename = schema.TextLine(title=_('File name'), description=_('Filename used on export'), required=True, default='memberdata.csv')
    delimiter = schema.TextLine(title=_('Delimiter'), description=_('Character to be used on                                                 export'), required=True, default=',')
    lineTerminator = schema.Choice(title=_('Line terminator'), description=_(''), required=True, vocabulary=LINETERMINATOR_VOCABULARY)
    encoding = schema.Choice(title=_('Encoding'), description=_(''), required=True, vocabulary=ENCODING_VOCABULARY)
    alwaysQuote = schema.Bool(title=_('Always quote fields?'), description=_('Should we always use quotes to separate data.'), default=False, required=True)


class ExportPanelAdapter(SchemaAdapterBase):
    __module__ = __name__
    adapts(IPloneSiteRoot)
    implements(IExportSchema)

    def __init__(self, context):
        super(ExportPanelAdapter, self).__init__(context)
        portal_properties = getToolByName(context, 'portal_properties')
        self.context = portal_properties.memberdataexport_properties

    delimiter = ProxyFieldProperty(IExportSchema['delimiter'])
    filename = ProxyFieldProperty(IExportSchema['filename'])

    def get_encoding(self):
        return self.context.encoding

    def set_encoding(self, value):
        self.context.manage_changeProperties(encoding=value)

    encoding = property(get_encoding, set_encoding)

    def get_lineTerminator(self):
        return self.context.lineTerminator

    def set_lineTerminator(self, value):
        self.context.manage_changeProperties(lineTerminator=value)

    lineTerminator = property(get_lineTerminator, set_lineTerminator)

    def get_alwaysQuote(self):
        return self.context.alwaysQuote

    def set_alwaysQuote(self, value):
        if value:
            self.context.manage_changeProperties(alwaysQuote=True)
        else:
            self.context.manage_changeProperties(alwaysQuote=False)

    alwaysQuote = property(get_alwaysQuote, set_alwaysQuote)


class ExportPanel(ControlPanelForm):
    __module__ = __name__
    form_fields = FormFields(IExportSchema)
    label = _('Member data export settings')
    description = _('Configure export settings for memberdata.')
    form_name = _('Export settings')
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/ads/content/Banner.py
# Compiled at: 2009-01-02 05:26:30
from AccessControl import ClassSecurityInfo
from Products.Archetypes.atapi import *
from zope.interface import implements
import interfaces
from Products.CMFDynamicViewFTI.browserdefault import BrowserDefaultMixin
from Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget import ReferenceBrowserWidget
from collective.ads.config import *
copied_fields = {}
copied_fields['effectiveDate'] = BaseSchema['effectiveDate'].copy()
copied_fields['effectiveDate'].schemata = 'default'
copied_fields['effectiveDate'].widget.label_msgid = 'Ads_label_effective'
copied_fields['expirationDate'] = BaseSchema['expirationDate'].copy()
copied_fields['expirationDate'].schemata = 'default'
copied_fields['expirationDate'].widget.label_msgid = 'Ads_label_expired'
schema = Schema((FileField(name='source', widget=FileWidget(description='Add Flash object', label='Source', label_msgid='Ads_label_source', description_msgid='Ads_help_source', i18n_domain='collective.ads'), required=0, storage=AttributeStorage()), ImageField(name='bannerimage', widget=ImageField._properties['widget'](description='Add images object like: jpg, gif or png', label='Image', label_msgid='Ads_label_image', description_msgid='Ads_help_image', i18n_domain='collective.ads'), required=0, storage=AttributeStorage(), max_size=(150,
                                                                                                                                                                                                                                                                                                 150), sizes={'small': (150, 150)}), IntegerField(name='clicks', widget=IntegerWidget(label='Maximum number of clicks', label_msgid='Ads_label_clicks', i18n_domain='collective.ads'), required=1), IntegerField(name='clicksUsed', default='0', widget=IntegerWidget(visible=-1, label='Clicksused', label_msgid='Ads_label_clicksUsed', i18n_domain='collective.ads')), IntegerField(name='percent', default='100', widget=IntegerWidget(label='Showing rate in %', label_msgid='Ads_label_percent', i18n_domain='collective.ads'), required=1), ReferenceField(name='linkIntern', widget=ReferenceBrowserWidget(allowed_types=('RichDocument',
                                                                               'File',
                                                                               'Image',
                                                                               'Folder'), label='Internal link', label_msgid='Ads_label_linkIntern', i18n_domain='collective.ads'), multiValued=0, relationship='banner_int_link'), StringField(name='linkExtern', validators=('isURL', ), widget=StringWidget(label='External Link', label_msgid='Ads_label_linkExtern', i18n_domain='collective.ads')), copied_fields['effectiveDate'], copied_fields['expirationDate']))
Banner_schema = BaseSchema.copy() + schema.copy()

class Banner(BaseContent, BrowserDefaultMixin):
    __module__ = __name__
    security = ClassSecurityInfo()
    implements(interfaces.IBanner)
    archetype_name = 'Banner'
    meta_type = 'Banner'
    _at_rename_after_creation = True
    schema = Banner_schema


registerType(Banner, PROJECTNAME)
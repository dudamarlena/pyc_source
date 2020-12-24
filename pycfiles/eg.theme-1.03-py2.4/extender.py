# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/eg/theme/extender.py
# Compiled at: 2010-11-18 04:43:28
from Products.Archetypes.public import *
from Products.Archetypes import atapi
from Products.ATContentTypes.interface import IATFolder
from Products.ATContentTypes.interface import IATDocument
from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from zope.component import adapts
from zope.interface import implements

class ShortTitleField(ExtensionField, StringField):
    __module__ = __name__


class ArticleTypeField(ExtensionField, StringField):
    __module__ = __name__


class ArticleLanguage(ExtensionField, StringField):
    __module__ = __name__


class OriginalArticleLanguage(ExtensionField, StringField):
    __module__ = __name__


class AvailableLanguages(ExtensionField, LinesField):
    __module__ = __name__


class Editor(ExtensionField, StringField):
    __module__ = __name__


class Publisher(ExtensionField, StringField):
    __module__ = __name__


class Translator(ExtensionField, StringField):
    __module__ = __name__


class TimeFrom(ExtensionField, IntegerField):
    __module__ = __name__


class TimeUntil(ExtensionField, IntegerField):
    __module__ = __name__


class Area(ExtensionField, LinesField):
    __module__ = __name__


class Topic(ExtensionField, LinesField):
    __module__ = __name__


class Licence(ExtensionField, StringField):
    __module__ = __name__


class UniqueCode(ExtensionField, StringField):
    __module__ = __name__


class URN(ExtensionField, StringField):
    __module__ = __name__


class DDC(ExtensionField, LinesField):
    __module__ = __name__


class PublicationDate(ExtensionField, DateTimeField):
    __module__ = __name__


class PreviewImage(ExtensionField, ImageField):
    __module__ = __name__


class MediaContentTypeField(ExtensionField, StringField):
    __module__ = __name__


class IsTranslation(ExtensionField, BooleanField):
    __module__ = __name__


class DocumentExtender(object):
    __module__ = __name__
    adapts(IATDocument)
    implements(ISchemaExtender)
    languages = [
     (
      'DE', 'German'), ('EN', 'English'), ('FR', 'French'), ('0', '--------'), ('AB', 'Abkhazian'), ('AA', 'Afar'), ('AF', 'Afrikaans'), ('SQ', 'Albanian'), ('AM', 'Amharic'), ('AR', 'Arabic'), ('HY', 'Armenian'), ('AS', 'Assamese'), ('AY', 'Aymara'), ('AZ', 'Azerbaijani'), ('BA', 'Bashkir'), ('EU', 'Basque'), ('BN', 'Bengali'), ('DZ', 'Bhutani'), ('BH', 'Bihari'), ('BI', 'Bislama'), ('BR', 'Breton'), ('BG', 'Bulgarian'), ('MY', 'Burmese'), ('BE', 'Byelorussian'), ('KM', 'Cambodian'), ('CA', 'Catalan'), ('ZH', 'Chinese'), ('CO', 'Corsican'), ('HR', 'Croatian'), ('CS', 'Czech'), ('DA', 'Danish'), ('NL', 'Dutch'), ('EO', 'Esperanto'), ('ET', 'Estonian'), ('FO', 'Faeroese'), ('FJ', 'Fiji'), ('FI', 'Finnish'), ('FR', 'French'), ('FY', 'Frisian'), ('GD', 'Gaelic'), ('GL', 'Galician'), ('KA', 'Georgian'), ('EL', 'Greek'), ('KL', 'Greenlandic'), ('GN', 'Guarani'), ('GU', 'Gujarati'), ('HA', 'Hausa'), ('IW', 'Hebrew'), ('HI', 'Hindi'), ('HU', 'Hungarian'), ('IS', 'Icelandic'), ('IN', 'Indonesian'), ('IA', 'Interlingua'), ('IE', 'Interlingue'), ('IK', 'Inupiak'), ('GA', 'Irish'), ('IT', 'Italian'), ('JA', 'Japanese'), ('JW', 'Javanese'), ('KN', 'Kannada'), ('KS', 'Kashmiri'), ('KK', 'Kazakh'), ('RW', 'Kinyarwanda'), ('KY', 'Kirghiz'), ('RN', 'Kirundi'), ('KO', 'Korean'), ('KU', 'Kurdish'), ('LO', 'Laothian'), ('LA', 'Latin'), ('LV', 'Latvian'), ('LN', 'Lingala'), ('LT', 'Lithuanian'), ('MK', 'Macedonian'), ('MG', 'Malagasy'), ('MS', 'Malay'), ('ML', 'Malayalam'), ('MT', 'Maltese'), ('MI', 'Maori'), ('MR', 'Marathi'), ('MO', 'Moldavian'), ('MN', 'Mongolian'), ('NA', 'Nauru'), ('NE', 'Nepali'), ('NO', 'Norwegian'), ('OC', 'Occitan'), ('OR', 'Oriya'), ('OM', 'Oromo'), ('PS', 'Pashto'), ('FA', 'Persian'), ('PL', 'Polish'), ('PT', 'Portuguese'), ('PA', 'Punjabi'), ('QU', 'Quechua'), ('RM', 'Rhaeto-Romance'), ('RO', 'Romanian'), ('RU', 'Russian'), ('SM', 'Samoan'), ('SG', 'Sangro'), ('SA', 'Sanskrit'), ('SR', 'Serbian'), ('SH', 'Serbo-Croatian'), ('ST', 'Sesotho'), ('TN', 'Setswana'), ('SN', 'Shona'), ('SD', 'Sindhi'), ('SI', 'Singhalese'), ('SS', 'Siswati'), ('SK', 'Slovak'), ('SL', 'Slovenian'), ('SO', 'Somali'), ('ES', 'Spanish'), ('SU', 'Sudanese'), ('SW', 'Swahili'), ('SV', 'Swedish'), ('TL', 'Tagalog'), ('TG', 'Tajik'), ('TA', 'Tamil'), ('TT', 'Tatar'), ('TE', 'Tegulu'), ('TH', 'Thai'), ('BO', 'Tibetan'), ('TI', 'Tigrinya'), ('TO', 'Tonga'), ('TS', 'Tsonga'), ('TR', 'Turkish'), ('TK', 'Turkmen'), ('TW', 'Twi'), ('UK', 'Ukrainian'), ('UR', 'Urdu'), ('UZ', 'Uzbek'), ('VI', 'Vietnamese'), ('VO', 'Volapuk'), ('CY', 'Welsh'), ('WO', 'Wolof'), ('XH', 'Xhosa'), ('JI', 'Yiddish'), ('YO', 'Yoruba'), ('ZU', 'Zulu')]
    fields = [
     ShortTitleField('shorttitle', widget=StringWidget(label='Short Title', il8n_domain='plone'), required=False, searchable=True), ArticleTypeField('articletype', widget=SelectionWidget(label='Article Type', il8n_domain='plone'), vocabulary=[('g', 'General'), ('mb', 'Media Description'), ('t', 'Thread'), ('be', 'Basic Element'), ('ub', 'Overview'), ('ve', 'In Depth Element')], required=False, searchable=True), MediaContentTypeField('mediacontent', widget=SelectionWidget(label='Media Content Type', description='If this is a Media Description please select the primary type of Content', il8n_domain='plone'), vocabulary=[('n', 'No Media Description'), ('a', 'Audio'), ('i', 'Image'), ('v', 'Video'), ('o', 'Other')], required=False, searchable=True), PreviewImage('previewimage', widget=ImageWidget(label='Preview Image', description='This image is used as preview for search result pages'), required=False, searchable=True), ArticleLanguage('articlelanguage', widget=atapi.SelectionWidget(label='Language', description='Which language is this article written in?'), vocabulary=languages, required=False, searchable=True), IsTranslation('istranslation', widget=atapi.BooleanWidget(label='This article is a translation from another language'), required=False, searchable=True), OriginalArticleLanguage('originallanguage', widget=atapi.SelectionWidget(label='Language of Original', description='Which language was this document translated from? If this is the original please select the same as above.'), vocabulary=languages, required=False, searchable=True), AvailableLanguages('availablelanguage', widget=atapi.PicklistWidget(label='Available Language', description='A list of all languages in which translations of this article are available', il8n_domain='pagetest'), vocabulary=languages, required=False, searchable=True), Editor('copyeditor', widget=atapi.StringWidget(label='Copy Editor', il8n_domain='plone'), required=False, searchable=True), Publisher('publisher', widget=atapi.StringWidget(label='Publisher', il8n_domain='plone'), required=False, searchable=True), Translator(name='translator', widget=atapi.StringWidget(label='Translator', label_msgid='pagetest_label_translator', il8n_domain='pagetest'), required=False, searchable=True), TimeFrom(name='timefrom', widget=atapi.IntegerWidget(label='Time interval from (year)', description='This determines the time interval that is used for advanced search queries', size=4, maxlength=4), required=False, searchable=True), TimeUntil(name='timeuntil', widget=atapi.IntegerWidget(label='until (year)', size=4, maxlength=4), required=False, searchable=True), Area(name='area', widget=atapi.PicklistWidget(label='Area'), vocabulary_factory='eg.theme.vocabularies.area', required=False, searchable=True), Topic(name='topic', widget=atapi.PicklistWidget(label='Topic'), vocabulary_factory='eg.theme.vocabularies.topics', required=False, searchable=True), Licence(name='licence', widget=atapi.SelectionWidget(label='Licence'), vocabulary=[('cr', 'All rights reserved'), ('by-nc-nd', 'by-nc-nd - Attribution, Noncommercial, No Derivative Works')], required=False, searchable=True), UniqueCode(name='unique', widget=atapi.StringWidget(label='Short URL without language code', description='e.g. If the URL is http://www.ieg-ego.eu/boeschf-2010-de please enter boeschf-2010 here', il8n_domain='plone'), required=False, searchable=True), URN(name='urn', widget=atapi.StringWidget(label='URN', description='URN without resolver. e.g. urn:nbn:de:0159-20100921115', il8n_domain='plone'), required=False, searchable=True), DDC(name='DDC', widget=atapi.LinesWidget(label='DDC', description='Enter the relevant DDC codes, one per line.', il8n_domain='plone', cols=10), required=False, searchable=True), PublicationDate(name='publicationsdate', widget=atapi.CalendarWidget(label='Publication date', description='Select the date that should appear as publication date in the page header', il8n_domain='plone', show_hm=False), required=False, searchable=True)]

    def __init__(self, context):
        self.context = context

    def getFields(self):
        return self.fields
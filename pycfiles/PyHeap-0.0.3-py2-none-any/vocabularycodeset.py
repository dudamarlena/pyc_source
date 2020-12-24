# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/vocabularycodeset.py
# Compiled at: 2016-01-05 10:24:49
from healthvaultlib.utils.xmlutils import XmlUtils
from healthvaultlib.objects.vocabularycodeitem import VocabularyCodeItem

class VocabularyCodeSet:
    """
        VocabularyCodeSet holds a vocabulary key details along with
        a list of vocabulary items.

        Attributes:
            name                Vocabulary name
            family              Vocabulary family
            version             Version
            code_item           Array of VocabularyCodeItem
            is_vocab_truncated  Indicates if list of vocabulary items in the 
                                vocabulary has been truncated.
            language            Language

    """

    def __init__(self, code_set_xml=None):
        """
            :param key_xml: lxml.etree.Element representing a single VocabularyCodeSet
        """
        self.name = None
        self.family = None
        self.version = None
        self.code_item = []
        self.is_vocab_truncated = None
        self.language = None
        if code_set_xml is not None:
            self.parse_xml(code_set_xml)
        return

    def parse_xml(self, xml):
        """
            :param key_xml: lxml.etree.Element representing a single VocabularyCodeSet
        """
        xmlutils = XmlUtils(xml)
        self.name = xmlutils.get_string_by_xpath('name')
        self.family = xmlutils.get_string_by_xpath('family')
        self.version = xmlutils.get_string_by_xpath('version')
        for item in xml.xpath('code-item'):
            self.code_item.append(VocabularyCodeItem(item))

        self.is_vocab_truncated = xmlutils.get_bool_by_xpath('is-vocab-truncated')
        self.language = xmlutils.get_lang()
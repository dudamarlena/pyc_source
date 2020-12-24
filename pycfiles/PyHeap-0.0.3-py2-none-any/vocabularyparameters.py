# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/healthvaultlib/objects/vocabularyparameters.py
# Compiled at: 2016-01-03 04:45:03
from lxml import etree

class VocabularyParameters:

    def __init__(self, keys):
        self.vocabulary_keys = keys
        self.fixed_culture = False

    def write_xml(self):
        params = etree.Element('vocabulary-parameters')
        for i in self.vocabulary_keys:
            params.append(i.write_xml())

        fixed_culture = etree.Element('fixed-culture')
        fixed_culture.text = 'false'
        if self.fixed_culture:
            fixed_culture.text = 'true'
        params.append(fixed_culture)
        return params
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
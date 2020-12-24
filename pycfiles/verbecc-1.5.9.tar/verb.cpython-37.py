# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\brett\git\verbecc\verbecc\verb.py
# Compiled at: 2019-07-28 19:37:52
# Size of source mod 2**32: 1285 bytes
from lxml import etree
from . import string_utils
from . import exceptions

class Verb:

    def __init__(self, v_elem):
        if v_elem.tag != 'v':
            raise exceptions.VerbsParserError('Unexpected element')
        try:
            self.predicted = False
            self.pred_score = 1.0
            self.infinitive = '' + v_elem.find('i').text
            self.infinitive_no_accents = string_utils.strip_accents(self.infinitive)
            self.template = '' + v_elem.find('t').text
            self.translation_en = ''
            en_node = v_elem.find('en')
            if en_node is not None:
                self.translation_en = '' + en_node.text
            self.impersonal = False
        except AttributeError as e:
            try:
                raise exceptions.VerbsParserError('Error parsing {}: {}'.format(etree.tostring(v_elem), str(e)))
            finally:
                e = None
                del e

    def __repr__(self):
        return 'infinitive={} infinitive_no_accents={} template={} translation_en={} impersonal={} predicted={} pred_score={}'.format(self.infinitive, self.infinitive_no_accents, self.template, self.translation_en, self.impersonal, self.predicted, self.pred_score)
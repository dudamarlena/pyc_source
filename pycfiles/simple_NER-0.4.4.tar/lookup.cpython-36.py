# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/lookup.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 1028 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from os import listdir
from os.path import join, dirname
import re

class LookUpNER(NERWrapper):

    def __init__(self, lang='en-us'):
        super().__init__()
        self.entities = {}
        self.load_entities(join(dirname(dirname(__file__)), 'res', lang))
        self.add_detector(self.annotate)

    def load_entities(self, folder):
        for entity_file in listdir(folder):
            if not entity_file.endswith('.entity'):
                pass
            else:
                with open(join(folder, entity_file)) as (f):
                    self.entities[entity_file.replace('.entity', '')] = f.read().lower().split('\n')

    def annotate(self, text):
        for label in self.entities:
            for ent in self.entities[label]:
                utt = re.sub('\\b' + ent + '\\b', '', text.lower())
                if utt != text.lower():
                    yield Entity(ent, label, source_text=text)
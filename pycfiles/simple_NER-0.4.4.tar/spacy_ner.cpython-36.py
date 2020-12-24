# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/spacy_ner.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 985 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
try:
    import spacy
except ImportError:
    print('you need to install spacy and download the model')
    print('pip install spacy')
    print('python -m spacy download en_core_web_md')
    raise

class SpacyNER(NERWrapper):

    def __init__(self, model='en_core_web_md'):
        super().__init__()
        self.add_detector(self.annotate)
        self.nlp = spacy.load(model)

    def annotate(self, text):
        doc = self.nlp(text)
        for entity in doc.ents:
            yield Entity((entity.text), (entity.label_), source_text=text)


if __name__ == '__main__':
    ner = SpacyNER()
    text = 'When Sebastian Thrun started working on self-driving cars at Google in 2007, few people outside of the company took him seriously.'
    for e in ner.extract_entities(text):
        print(e.value, e.entity_type)
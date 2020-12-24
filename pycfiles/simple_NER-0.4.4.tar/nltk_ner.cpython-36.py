# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/nltk_ner.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 1436 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
try:
    import nltk
    nltk.download('punkt')
    nltk.download('averaged_perceptron_tagger')
    nltk.download('maxent_ne_chunker')
    nltk.download('words')
except ImportError:
    print('you need to install nltk')
    print('pip install nltk')
    raise

class NltkNER(NERWrapper):

    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)

    def annotate(self, text):
        words = nltk.word_tokenize(text)
        tagged_Words = nltk.pos_tag(words)
        named_Entity = nltk.ne_chunk(tagged_Words)
        for x in named_Entity:
            if isinstance(x, nltk.tree.Tree):
                data = {'label':x.__dict__['_label'], 
                 'pos_tag':[e[1] for e in x], 
                 'tokens':[e[0] for e in x]}
                yield Entity((' '.join([e[0] for e in x])), (x.__dict__['_label']),
                  source_text=text,
                  data=data)


if __name__ == '__main__':
    from pprint import pprint
    ner = NltkNER()
    text = 'The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world".'
    for r in ner.extract_entities(text):
        print(r.value, r.entity_type)
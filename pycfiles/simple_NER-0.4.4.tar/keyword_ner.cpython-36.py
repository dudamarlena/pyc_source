# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/keyword_ner.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 937 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
from simple_NER.annotators.utils.keywords.rake import Rake

class KeywordNER(NERWrapper):

    def __init__(self):
        super().__init__()
        self.add_detector(self.annotate)
        self.rake = Rake()

    def annotate(self, text):
        for x in self.rake.run(text):
            data = {'score': x[1]}
            yield Entity((x[0]), 'keyword',
              source_text=text,
              data=data)


if __name__ == '__main__':
    from pprint import pprint
    ner = KeywordNER()
    text = 'The Israeli Prime Minister Benjamin Netanyahu has warned that Iran poses a "threat to the entire world".'
    for r in ner.extract_entities(text):
        pprint(r.as_json())
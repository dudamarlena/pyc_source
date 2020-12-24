# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/remote/dbpedia.py
# Compiled at: 2019-12-12 21:17:29
# Size of source mod 2**32: 1682 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
try:
    import spotlight
except ImportError:
    print('you need to install pyspotlight')
    print('pip install pyspotlight')
    raise

class SpotlightNER(NERWrapper):

    def __init__(self, host='http://api.dbpedia-spotlight.org/en/annotate', confidence=0.4, support=20):
        super().__init__()
        self.host = host
        self.confidence = confidence
        self.support = support
        self.add_detector(self.annotate)

    def annotate(self, text):
        for e in spotlight.annotate((self.host), text, confidence=(self.confidence),
          support=(self.support)):
            for e_type in e['types'].split(','):
                if e_type.startswith('DBpedia:'):
                    yield Entity((e['surfaceForm']), (e_type.split(':')[(-1)]), source_text=text,
                      data={'uri':e['URI'], 
                     'support':e['support'], 
                     'offset':e['offset'], 
                     'percentageOfSecondRank':e['percentageOfSecondRank'], 
                     'similarityScore':e['similarityScore'], 
                     'types':e['types'].split(',')},
                      confidence=(e['similarityScore']))


if __name__ == '__main__':
    ner = SpotlightNER()
    for r in ner.extract_entities('elon musk works in spaceX'):
        print(r.value, r.entity_type)
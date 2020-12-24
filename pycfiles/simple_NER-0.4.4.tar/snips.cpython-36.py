# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/user/PycharmProjects/simple_NER/simple_NER/annotators/snips.py
# Compiled at: 2020-02-23 15:19:35
# Size of source mod 2**32: 1298 bytes
from simple_NER.annotators import NERWrapper
from simple_NER import Entity
try:
    from snips_nlu.entity_parser import BuiltinEntityParser
except ImportError:
    print('you need to install snips_nlu')
    print('pip install snips-nlu')
    print('python -m snips_nlu download end')
    raise

class SnipsNER(NERWrapper):

    def __init__(self, lang='en'):
        super().__init__()
        self.engine = BuiltinEntityParser.build(language=lang)

    def extract_entities(self, text, as_json=False):
        parsed = self.engine.parse(text)
        for e in parsed:
            yield Entity((e['value']), (e['entity_kind']),
              source_text=text,
              data=(e['resolved_value']))


if __name__ == '__main__':
    ner = SnipsNER()
    from pprint import pprint
    text = 'What will be the weather in San Francisco next week?'
    text = '"Helicopters will patrol the temporary no-fly zone around \n    New Jersey\'s MetLife Stadium Sunday, with F-16s based in Atlantic City \n    ready to be scrambled if an unauthorized aircraft does enter the \n    restricted airspace'
    for r in ner.extract_entities(text):
        print(r.value, r.entity_type)
        pprint(r.as_json())
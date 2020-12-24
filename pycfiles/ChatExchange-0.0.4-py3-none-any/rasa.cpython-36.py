# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\adapters\rasa.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 2670 bytes
import json
from chatette_qiu.units import ENTITY_MARKER
from chatette_qiu.utils import cast_to_unicode
from ._base import Adapter

class RasaAdapter(Adapter):

    def __init__(self, batch_size=10000):
        super(RasaAdapter, self).__init__(batch_size)

    def _get_file_extension(self):
        return 'json'

    def prepare_example(self, example):

        def entity_to_rasa(entity):
            entity['text'] = entity['text'].strip()
            first_index = self._RasaAdapter__find_entity(example.text, entity['text'])
            example.text = example.text[:first_index] + example.text[first_index + len(ENTITY_MARKER):]
            return {'value':entity['value'], 
             'entity':entity['slot-name'], 
             'start':first_index, 
             'end':first_index + len(entity['text'])}

        return {'intent':example.name, 
         'entities':[entity_to_rasa(e) for e in example.entities], 
         'text':example.text}

    def _write_batch(self, output_file_handle, batch):
        rasa_entities = [self.prepare_example(ex) for ex in batch.examples]
        json_data = {'rasa_nlu_data': {'common_examples':rasa_entities, 
                           'regex_features':[],  'entity_synonyms':self._RasaAdapter__synonym_format(batch.synonyms)}}
        json_data = cast_to_unicode(json_data)
        output_file_handle.write(json.dumps(json_data, ensure_ascii=False, indent=2,
          sort_keys=True))

    @classmethod
    def __synonym_format(cls, synonyms):
        return [{'value':slot_name,  'synonyms':synonyms[slot_name]} for slot_name in synonyms if len(synonyms[slot_name]) > 1]

    @staticmethod
    def __find_entity(text, entity_str):
        """
        Finds the entity `entity_str` in `text`
        ignoring the case of the first non-space.
        """
        index = text.find(ENTITY_MARKER + entity_str)
        if index == -1:
            return text.lower().find(entity_str.lower())
        else:
            return index
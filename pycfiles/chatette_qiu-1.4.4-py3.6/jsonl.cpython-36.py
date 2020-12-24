# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\adapters\jsonl.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 1565 bytes
import io, json, os
from chatette_qiu.utils import cast_to_unicode
from chatette_qiu.units import ENTITY_MARKER
from ._base import Adapter

class JsonListAdapter(Adapter):

    def _get_file_extension(self):
        return 'jsonl'

    def prepare_example(self, example):
        example.text = example.text.replace(ENTITY_MARKER, '')
        return json.dumps((cast_to_unicode(example.__dict__)), ensure_ascii=False, sort_keys=True)

    def _write_batch(self, output_file_handle, batch):
        output_file_handle.writelines([self.prepare_example(example) + '\n' for example in batch.examples])

    def write(self, output_directory, examples, synonyms):
        super(JsonListAdapter, self).write(output_directory, examples, synonyms)
        processed_synonyms = self._JsonListAdapter__synonym_format(synonyms)
        if processed_synonyms is not None:
            synonyms_file_path = os.path.join(output_directory, 'synonyms.json')
            with io.open(synonyms_file_path, 'w') as (output_file):
                output_file.write(json.dumps((cast_to_unicode(processed_synonyms)), ensure_ascii=False,
                  sort_keys=True,
                  indent=2))

    @classmethod
    def __synonym_format(cls, synonyms):
        result = {key:values for key, values in synonyms.items() if len(values) > 1 or values[0] != key if len(values) > 1 or values[0] != key}
        if not result:
            return
        else:
            return result
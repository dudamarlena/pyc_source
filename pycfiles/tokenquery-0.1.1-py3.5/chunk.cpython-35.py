# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/models/chunk.py
# Compiled at: 2017-01-06 20:27:14
# Size of source mod 2**32: 1299 bytes
import re

class Chunk:
    __doc__ = ' Any sequence of tokens that shares a label,\n        this can be used to stote sentences, entities\n        and ...\n    '

    def __init__(self, chunk_id, tokens):
        self.chunk_id = chunk_id
        self.tokens = tokens
        self.start_span, self.end_span, self.text = change_tokenlist_to_chunk(tokens)

    def change_tokenlist_to_chunk(self, token_list):
        if not token_list:
            return
        start_span = token_list[0].span_start
        end_span = token_list[0].span_end
        string = token_list[0].get_text()
        if len(token_list) == 1:
            return (start_span, end_span, string)
        for token in token_list[1:]:
            end_span = token.span_end
            string += ' ' + token.get_text()

        return (start_span, end_span, string)

    def add_a_label(self, label_name, label_value):
        for counter, token in enumerate(self.tokens):
            if counter == 0:
                token.add_a_label(label_name + '~B', label_value)
            else:
                token.add_a_label(label_name + '~I', label_value)

    def get_a_label(self, label_name):
        return self.tokens[0].get_a_label(label_name)

    def get_text(self):
        return self.text
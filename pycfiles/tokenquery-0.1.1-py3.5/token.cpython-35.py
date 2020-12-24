# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/tokenquery/models/token.py
# Compiled at: 2017-01-28 21:15:31
# Size of source mod 2**32: 1156 bytes


class Token:

    def __init__(self, token_id, token_text, span_start, span_end):
        self.token_id = token_id
        self.token_text = token_text
        self.span_start = span_start
        self.span_end = span_end
        self.labels = {}

    def get_token_id(self):
        return self.token_id

    def set_token_id(self, token_id):
        self.token_id = token_id

    def add_a_label(self, label_name, label_value):
        self.labels[label_name] = label_value

    def get_a_label(self, label_name):
        return self.labels.get(label_name, None)

    def set_text(self, text):
        self.token_text = text

    def get_text(self):
        return self.token_text

    def set_span(self, span_start, span_end):
        self.span_start = span_start
        self.span_end = span_end

    def get_span(self):
        return (
         self.span_start, self.span_end)

    def print_token(self):
        print('token_id', self.token_id)
        print('token_text', self.token_text)
        print('span_start', self.span_start)
        print('span_end', self.span_end)
        for label in self.labels:
            print(label, self.labels[label])
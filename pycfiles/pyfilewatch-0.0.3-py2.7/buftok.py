# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/filewatch/buftok.py
# Compiled at: 2015-01-11 19:32:27


class BufferedTokenizer:

    def __init__(self, delimiter='\n', size_limit=None):
        self.delimiter = delimiter
        self.size_limit = size_limit
        self.input = []
        self.input_size = 0

    def extract(self, data):
        """Extract takes an arbitrary string of input data and returns an array of
        tokenized entities, provided there were any available to extract. """
        entities = data.split(self.delimiter, -1)
        if self.size_limit:
            if self.input_size + len(entities[0]) > self.input_size:
                raise Exception('input buffer full')
        self.input.append(entities.pop(0))
        if not entities:
            return []
        entities.insert(0, ('').join(self.input))
        self.input = []
        self.input.append(entities.pop())
        if self.size_limit:
            self.input_size = len(self.input.first)
        return entities

    def flush(self):
        """Flush the contents of the input buffer, i.e. return the input buffer
        even though a token has not yet been encountered"""
        buffer = ('').join(self.input)
        self.input = []
        if self.size_limit:
            self.input_size = 0
        return buffer

    def empty(self):
        return len(self.input) == 0
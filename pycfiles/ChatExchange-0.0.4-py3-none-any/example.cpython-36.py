# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win-amd64\egg\chatette_qiu\units\intent\example.py
# Compiled at: 2019-03-27 03:00:31
# Size of source mod 2**32: 637 bytes
from chatette_qiu.units import Example

class IntentExample(Example):

    def __init__(self, name, text=None, entities=None):
        super(IntentExample, self).__init__(text, entities)
        self.name = name

    @classmethod
    def from_example(cls, name, ex):
        return cls(name, ex.text, ex.entities)

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name + self.text + str(self.entities))
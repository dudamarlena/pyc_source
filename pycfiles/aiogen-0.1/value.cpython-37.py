# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/aiogcd/orm/properties/value.py
# Compiled at: 2019-10-22 09:03:49
# Size of source mod 2**32: 1507 bytes
__doc__ = 'value.py\n\nCreated on: May 19, 2017\n    Author: Jeroen van der Heijden <jeroen@transceptor.technology>\n'
from connector.entity import Entity
from connector.utils import value_to_dict

class Value:

    def __init__(self, default=None, required=True):
        self.default = default
        self.required = required
        self.name = None

    @property
    def ascending(self):
        return (
         self.name, 'ASCENDING')

    @property
    def descending(self):
        return (
         self.name, 'DESCENDING')

    def check_value(self, value):
        raise NotImplementedError()

    def get_value(self, model):
        return model.__dict__.get(self.name, None)

    def set_value(self, model, value):
        Entity.set_property(model, self.name, value)

    def _compare(self, other, op):
        self.check_value(other)
        return {'property':{'name': self.name}, 
         'value':value_to_dict(other), 
         'op':op}

    def __eq__(self, other):
        return self._compare(other, 'EQUAL')

    def __ne__(self, other):
        raise Exception('Cannot use NOT EQUAL in a filter expression')

    def __lt__(self, other):
        return self._compare(other, 'LESS_THAN')

    def __le__(self, other):
        return self._compare(other, 'LESS_THAN_OR_EQUAL')

    def __gt__(self, other):
        return self._compare(other, 'GREATER_THAN')

    def __ge__(self, other):
        return self._compare(other, 'GREATER_THAN_OR_EQUAL')
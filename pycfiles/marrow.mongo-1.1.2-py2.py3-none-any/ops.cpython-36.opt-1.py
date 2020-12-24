# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/query/ops.py
# Compiled at: 2017-05-17 14:49:33
# Size of source mod 2**32: 5096 bytes
"""MongoDB filter, projection, and update operation helpers.

These encapsulate the functionality of creating combinable mappings 
"""
from __future__ import unicode_literals
from collections import Mapping, MutableMapping
from copy import deepcopy
from ...schema.compat import odict, py3
from ..util import SENTINEL

class Ops(MutableMapping):
    __slots__ = ('operations', 'collection', 'document')

    def __init__(self, operations=None, collection=None, document=None):
        self.operations = operations or odict()
        self.collection = collection
        self.document = document

    def __repr__(self, extra=None):
        return '{}({}{}{}{})'.format(self.__class__.__name__, repr([(i, j) for i, j in self.operations.items()]), ', collection={}'.format(self.collection) if self.collection else '', ', document={}'.format(self.document) if self.document else '', extra or '')

    @property
    def as_query(self):
        return self.operations

    def __getitem__(self, name):
        return self.operations[name]

    def __setitem__(self, name, value):
        self.operations[name] = value

    def __delitem__(self, name):
        del self.operations[name]

    def __iter__(self):
        return iter(self.operations.keys())

    def __len__(self):
        return len(self.operations)

    if py3:

        def keys(self):
            return self.operations.keys()

        def items(self):
            return self.operations.items()

        def values(self):
            return self.operations.values()

    else:

        def keys(self):
            return self.operations.iterkeys()

        def items(self):
            return self.operations.iteritems()

        def values(self):
            return self.operations.itervalues()

    def __contains__(self, key):
        return key in self.operations

    def __eq__(self, other):
        return self.operations == other

    def __ne__(self, other):
        return self.operations != other

    def get(self, key, default=None):
        return self.operations.get(key, default)

    def clear(self):
        self.operations.clear()

    def pop(self, name, default=SENTINEL):
        if default is SENTINEL:
            return self.operations.pop(name)
        else:
            return self.operations.pop(name, default)

    def popitem(self):
        return self.operations.popitem()

    def update(self, *args, **kw):
        (self.operations.update)(*args, **kw)

    def setdefault(self, key, value=None):
        return self.operations.setdefault(key, value)

    def copy(self):
        """Return a shallow copy."""
        return self.__class__(self.operations.copy(), self.collection, self.document)


class Filter(Ops):
    __slots__ = ('operations', 'collection', 'document')

    def __and__(self, other):
        """Boolean AND joining of filter operations."""
        operations = deepcopy(self.operations)
        other = other.as_query if hasattr(other, 'as_query') else other
        for k, v in other.items():
            if k not in operations:
                operations[k] = v
                continue
                if k == '$and':
                    operations.setdefault('$and', [])
                    operations['$and'].extend(v)
                    continue
                else:
                    if k == '$or':
                        operations.setdefault('$and', [])
                        operations['$and'].append(odict(((k, v),)))
                        if '$or' in operations:
                            operations['$and'].append(odict((('$or', operations.pop('$or')),)))
                            continue
                if not isinstance(operations[k], Mapping):
                    operations[k] = odict((('$eq', operations[k]),))
                if not isinstance(v, Mapping):
                    v = odict((('$eq', v),))
                operations[k].update(v)

        return self.__class__(operations=operations, collection=(self.collection), document=(self.document))

    def __or__(self, other):
        operations = deepcopy(self.operations)
        other = other.as_query if hasattr(other, 'as_query') else other
        if len(operations) == 1 and '$or' in operations:
            operations['$or'].append(other)
            return self.__class__(operations=operations,
              collection=(self.collection),
              document=(self.document))
        else:
            return self.__class__(operations={'$or': [operations, other]},
              collection=(self.collection),
              document=(self.document))

    def __invert__(self):
        """Return the boolean inversion of the current query.
                
                Equivalent to the MongoDB `$not` operator.
                """
        operations = deepcopy(self.operations)
        return self.__class__(operations={'$not': operations},
          collection=(self.collection),
          document=(self.document))


class Update(Ops):
    __slots__ = ('operations', 'collection', 'document')
    EACH_COMBINING = {
     '$addToSet', '$push'}

    def __init__(self, operations=None, collection=None, document=None):
        self.operations = operations or odict()
        self.collection = collection
        self.document = document

    def __and__(self, other):
        operations = deepcopy(odict(other.operations if hasattr(other, 'operations') else other))
        for op in self:
            for field in self[op]:
                operations.setdefault(op, odict())
                operations[op][field] = self[op][field]

        return self.__class__(operations=operations, collection=(self.collection), document=(self.document))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/param/common.py
# Compiled at: 2017-09-13 15:15:35
# Size of source mod 2**32: 1646 bytes
"""Parameterized support akin to Django's ORM or MongoEngine."""
from __future__ import unicode_literals
from ...package.loader import traverse
from ...schema.compat import odict

def _deferred_method(name, _named=None, **kw):

    def _deferred_method_inner(self, other):
        if _named:
            if not len(_named) == len(other):
                raise TypeError('Incorrect number of arguments.')
            values = iter(other)
            for i in _named:
                kw[i] = next(values)

            return (getattr(self, name))(**kw)
        else:
            return (getattr(self, name))(other, **kw)

    return _deferred_method_inner


def _operator_choice(conversion, lookup, **kw):

    def _operator_choice_inner(self, other):
        return (lookup[conversion(other)])(self, **kw)

    return _operator_choice_inner


def _process_arguments(Document, prefixes, suffixes, arguments, passthrough=None):
    for name, value in arguments.items():
        prefix, _, nname = name.partition('__')
        if prefix in prefixes:
            name = nname
        nname, _, suffix = name.rpartition('__')
        if suffix in suffixes:
            name = nname
        field = traverse(Document, name.replace('__', '.'))
        if passthrough:
            if not passthrough & {prefix, suffix}:
                value = field._field.transformer.foreign(value, (field, Document))
        yield (
         prefixes.get(prefix or None, None), suffixes.get(suffix, None), field, value)


def _current_date(value):
    if value in ('ts', 'timestamp'):
        return {'$type': 'timestamp'}
    else:
        return True


def _bit(op):

    def bitwiseUpdate(value):
        return odict({op: int(value)})

    return bitwiseUpdate
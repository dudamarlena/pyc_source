# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /marrow/mongo/param/update.py
# Compiled at: 2017-05-17 14:49:33
# Size of source mod 2**32: 4314 bytes
"""Parameterized support akin to Django's ORM or MongoEngine."""
from __future__ import unicode_literals
from collections import Mapping
from operator import __neg__
from ...schema.compat import unicode
from ..query import Update
from .common import _bit, _current_date, _process_arguments
DEFAULT_UPDATE = 'set'

def _push_each(value, field):
    value = list(field.transformer.foreign(v, (field, field.__document__)) for v in value)
    return {'$each': value}


def _push_slice(value):
    return {'$slice': int(value)}


def _push_sort(value):
    return {'$sort': value}


def _push_position(value):
    return {'$position': int(value)}


UPDATE_MAGIC = {
 _push_each}
UPDATE_ALIASES = {'add':'inc', 
 'add_to_set':'addToSet', 
 'bit_and':(
  'bit', _bit('and')), 
 'bit_or':(
  'bit', _bit('or')), 
 'bit_xor':(
  'bit', _bit('xor')), 
 'currentDate':(
  'currentDate', _current_date), 
 'current_date':(
  'currentDate', _current_date), 
 'dec':(
  'inc', __neg__), 
 'now':(
  'currentDate', _current_date), 
 'pull_all':'pullAll', 
 'push_all':'pushAll', 
 'push_each':(
  'push', _push_each), 
 'push_pos':(
  'push', _push_position), 
 'push_position':(
  'push', _push_position), 
 'push_slice':(
  'push', _push_slice), 
 'push_sort':(
  'push', _push_sort), 
 'rename':(
  'rename', unicode), 
 'set_on_insert':'setOnInsert', 
 'soi':'setOnInsert', 
 'sub':(
  'inc', __neg__)}
UPDATE_ALIASES.update({i:i for i in frozenset({'setOnInsert', 'pullAll', 'push', 'rename', 'pushAll', 'inc', 'max', 'mul', 'min', 'set', 'pull', 'unset', 'bit'})})
UPDATE_PASSTHROUGH = {
 'bit',
 'currentDate',
 'pull',
 'push',
 'push_each',
 'push_pos',
 'push_position',
 'push_slice',
 'push_sort',
 'rename',
 'unset'}

def U(Document, __raw__=None, **update):
    """Generate a MongoDB update document through paramater interpolation.
        
        Arguments passed by name have their name interpreted as an optional operation prefix (defaulting to `set`, e.g.
        `push`), a double-underscore separated field reference (e.g. `foo`, or `foo__bar`, or `foo__S__bar`, or
        `foo__27__bar`)
        
        Because this utility is likely going to be used frequently it has been given a single-character name.
        """
    ops = Update(__raw__)
    args = _process_arguments(Document, UPDATE_ALIASES, {}, update, UPDATE_PASSTHROUGH)
    for operation, _, field, value in args:
        if not operation:
            operation = DEFAULT_UPDATE
        else:
            if isinstance(operation, tuple):
                operation, cast = '$' + operation[0], operation[1]
                if cast in UPDATE_MAGIC:
                    value = cast(value, field)
                else:
                    value = cast(value)
                if operation in ops:
                    if ~field in ops[operation]:
                        if isinstance(value, Mapping):
                            ops[operation][(~field)].update(value)
                            continue
            else:
                operation = '$' + operation
        ops &= Update({operation: {~field: value}})

    return ops
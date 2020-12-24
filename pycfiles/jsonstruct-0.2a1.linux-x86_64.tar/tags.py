# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/jsonstruct/tags.py
# Compiled at: 2013-08-09 10:47:32
"""The jsonstruct.tags module provides the custom tags
used for pickling and unpickling Python objects.

These tags are keys into the flattened dictionaries
created by the Pickler class.  The Unpickler uses
these custom key names to identify dictionaries
that need to be specially handled.
"""
from jsonstruct.compat import set
ID = 'py/id'
OBJECT = 'py/object'
TYPE = 'py/type'
REPR = 'py/repr'
REF = 'py/ref'
TUPLE = 'py/tuple'
SET = 'py/set'
SEQ = 'py/seq'
STATE = 'py/state'
RESERVED = set([OBJECT, TYPE, REPR, REF, TUPLE, SET, SEQ, STATE])
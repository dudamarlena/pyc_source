# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/resolver/resolvers.py
# Compiled at: 2015-04-17 13:50:21
from .key import KeyResolver
from pathresolver.exceptions import UnableToResolve
from .predicate import PredicateResolver
from .predicate import StringMatchResolver
from .multi import MultiKeyResolver
MATCH_ALL = '*'
attribute_resolver = KeyResolver(lambda k, v: getattr(v, k), (AttributeError, TypeError))
key_lookup_resolver = KeyResolver(lambda k, v: v[k], (KeyError, TypeError))
index_lookup_resolver = KeyResolver(lambda k, v: v[int(k)], (KeyError, IndexError, TypeError, ValueError))
match_all_dict_resolver = PredicateResolver(lambda _, dct: dct.values(), AttributeError, dict)
match_all_iterable_resolver = PredicateResolver(lambda _, iterable: [i for i in iterable], (
 AttributeError, TypeError), lambda _, value: hasattr(value, '__iter__') or hasattr(value, '__getitem__'))
basic_multi_resolver = MultiKeyResolver(attribute_resolver, key_lookup_resolver, index_lookup_resolver)
match_all_resolver = StringMatchResolver(MultiKeyResolver(match_all_dict_resolver, match_all_iterable_resolver), UnableToResolve, MATCH_ALL)
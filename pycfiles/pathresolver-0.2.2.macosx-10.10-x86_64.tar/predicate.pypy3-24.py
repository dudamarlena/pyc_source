# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/resolver/predicate.py
# Compiled at: 2015-04-17 13:50:21
from .key import KeyResolver
from pathresolver.exceptions import UnableToResolve

class PredicateResolver(KeyResolver):

    def __init__(self, func, failure_exc, predicate_or_klass):
        self.predicate_or_klass = predicate_or_klass
        super(PredicateResolver, self).__init__(func, failure_exc)

    def predicate_success(self, key, value):
        if isinstance(self.predicate_or_klass, (tuple, type)):
            return isinstance(value, self.predicate_or_klass)
        else:
            return self.predicate_or_klass(key, value)

    def resolve(self, key, value):
        if self.predicate_success(key, value):
            return super(PredicateResolver, self).resolve(key, value)
        raise UnableToResolve('Cannot find {key} in {value}'.format(key=key, value=value))


class StringMatchResolver(PredicateResolver):

    def __init__(self, func, failure_exc, match_string):
        super(StringMatchResolver, self).__init__(func, failure_exc, lambda key, _: key == match_string)
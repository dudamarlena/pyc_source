# uncompyle6 version 3.7.4
# PyPy Python bytecode 3.2 (3187)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/andrewcrosio/projects/pathresolver/pypy3/site-packages/pathresolver/evaluator/find.py
# Compiled at: 2015-04-17 13:50:21
from pathresolver.exceptions import NoMatchError, UnableToResolve
from pathresolver.resolver import basic_multi_resolver
from pathresolver.resolver import match_all_resolver as _match_all_resolver
from .base import EvaluatorBase
from .base import NO_DEFAULT
IGNORE_VALUE = object()

class Finder(EvaluatorBase):

    def __init__(self, resolver=basic_multi_resolver, match_all_resolver=_match_all_resolver):
        self.resolver = resolver
        self.match_all_resolver = match_all_resolver

    def resolve(self, current_key, next_key, value, default=NO_DEFAULT):
        call_as_func = False
        if current_key.endswith('()'):
            current_key = current_key[:-2]
            call_as_func = True
        try:
            iterable = self.match_all_resolver.resolve(current_key, value)
        except UnableToResolve:
            next_value = self.resolver.resolve(current_key, value)
            if call_as_func:
                next_value = next_value()
            evaluated_value = self.evaluate(next_value, next_key, default=default)
        else:
            if call_as_func:
                raise NotImplementedError()
            evaluated_value = (self.evaluate(next_value, next_key, default=IGNORE_VALUE) for next_value in iterable)
            evaluated_value = [value for value in evaluated_value if value is not IGNORE_VALUE]
            if not evaluated_value:
                if default is NO_DEFAULT:
                    raise UnableToResolve()
                evaluated_value = default
            return evaluated_value

    def evaluate(self, value, path, default=NO_DEFAULT):
        if not path:
            return value
        try:
            current_key, next_key = path.split('.', 1)
        except ValueError:
            current_key = path
            next_key = None

        try:
            try:
                evaluated_value = self.resolve(current_key, next_key, value, default=default)
            except (NoMatchError, UnableToResolve):
                if not callable(value):
                    raise
                value = value()
                evaluated_value = self.resolve(current_key, next_key, value, default=default)

        except (NoMatchError, UnableToResolve) as error:
            if default is NO_DEFAULT:
                if isinstance(error, NoMatchError):
                    root = error.root
                    index = error.index + 1
                else:
                    root = current_key
                    index = 0
                raise NoMatchError('Unable to find {} in {} at index'.format(path, value, index), root, index)
            evaluated_value = default

        return evaluated_value
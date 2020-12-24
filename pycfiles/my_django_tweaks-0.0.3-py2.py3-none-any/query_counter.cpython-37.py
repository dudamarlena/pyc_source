# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ricard/develop/my_django_tweaks/my_django_tweaks/test_utils/query_counter.py
# Compiled at: 2019-05-17 08:43:05
# Size of source mod 2**32: 3076 bytes
from django.conf import settings
from django.db.backends.utils import CursorWrapper
import contextlib, re, traceback, warnings

class TooManySQLQueriesException(Exception):
    pass


class TestQueryCounter(object):
    _TestQueryCounter__instance = None

    def __new__(cls, *args, **kwargs):
        if TestQueryCounter._TestQueryCounter__instance is None:
            TestQueryCounter._TestQueryCounter__instance = object.__new__(cls)
            TestQueryCounter._TestQueryCounter__instance.reset()
        return TestQueryCounter._TestQueryCounter__instance

    def new_query(self, sql, params, stack):
        for pattern in getattr(settings, 'TEST_QUERY_COUNTER_IGNORE_PATTERNS', ['.*SAVEPOINT.*']):
            if re.match(pattern, sql):
                return

        self._counter += 1
        self._queries_stack.append((sql, params, stack))

    def reset(self):
        self._counter = 0
        self._queries_stack = []
        self._frozen = False

    def get_counter(self):
        return self._counter

    def get_queries_stack(self):
        return self._queries_stack

    @contextlib.contextmanager
    def freeze():
        instance = TestQueryCounter()
        prev_frozen = instance._frozen
        instance._frozen = True
        try:
            yield
        finally:
            instance._frozen = prev_frozen


def hacked_execute(self, sql, params=()):
    counter = TestQueryCounter()
    if not counter._frozen:
        counter.new_query(sql, params, traceback.format_stack(limit=10)[:8])
    return self.old_execute(sql, params)


class query_counter(object):

    def __enter__(self):
        TestQueryCounter().reset()
        CursorWrapper.old_execute = CursorWrapper.execute
        CursorWrapper.execute = hacked_execute

    def __exit__(self, exc_type, exc_val, exc_tb):
        CursorWrapper.execute = CursorWrapper.old_execute
        if exc_type is None:
            test_query_counter = TestQueryCounter().get_counter()
            if test_query_counter > getattr(settings, 'TEST_QUERY_NUMBER_RAISE_ERROR', 15):
                if getattr(settings, 'TEST_QUERY_NUMBER_PRINT_QUERIES', False):
                    print('=================== Query Stack ===================')
                    for query in TestQueryCounter().get_queries_stack():
                        print(query[:2])
                        print(''.join(query[2]))
                        print()

                    print('===================================================')
                raise TooManySQLQueriesException('Too many queries executed: %d' % test_query_counter)
            else:
                if test_query_counter > getattr(settings, 'TEST_QUERY_NUMBER_SHOW_WARNING', 10):
                    warnings.warn('High number of queries executed: %d' % test_query_counter)
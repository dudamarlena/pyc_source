# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/Infinidat/infi.pyutils/tests/test__contexts.py
# Compiled at: 2016-09-14 06:55:36
from .test_utils import TestCase
import inspect
from infi.pyutils.contexts import contextmanager

@contextmanager
def example_context_manager(a, b, c):
    """context_manager_docstring"""
    yield 2


class ContextmanagerTestCase(TestCase):

    def test__contextmanager(self):
        self.assertEquals(example_context_manager.__doc__, 'context_manager_docstring')
        self.assertEquals(example_context_manager.__name__, 'example_context_manager')
        self.assertEquals(inspect.getargspec(example_context_manager).args, ['a', 'b', 'c'])
        with example_context_manager(1, 2, 3) as (result):
            pass
        self.assertEquals(result, 2)
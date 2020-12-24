# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/test_resolver.py
# Compiled at: 2007-05-28 18:58:50
"""
Test the task resolution mechanisms.
"""
from mkcode import resolver, registry
from nose import with_setup

def clear_registry():
    registry.clear()


class FakeTask(object):
    __module__ = __name__

    def __init__(self, name, deps=None):
        self.name = name
        if not deps:
            deps = []
        self.dependencies = deps
        registry.tasks[name] = self


@with_setup(clear_registry)
def test_trivial_path_to_goal():
    t = FakeTask('x')
    path = resolver.path_to_goal(t)
    assert path == [t]


@with_setup(clear_registry)
def test_path_to_nested_tasks():
    t = FakeTask('t')
    a = FakeTask('a', [t])
    path = resolver.path_to_goal(a)
    assert path == [t, a]


@with_setup(clear_registry)
def test_exclusion_of_repeated_dependancies():
    a = FakeTask('a')
    b = FakeTask('b', [a])
    c = FakeTask('c', [b, a])
    path = resolver.path_to_goal(c)
    assert path == [a, b, c]
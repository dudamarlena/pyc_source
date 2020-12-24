# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/testoob/extracting.py
# Compiled at: 2009-10-07 18:08:46
"""Extracting tests from a test suite"""
from __future__ import generators
try:
    from itertools import ifilter as _ifilter
except ImportError:
    from compatibility.itertools import ifilter as _ifilter

def _breadth_first(tree, children=iter):
    """Traverse the nodes of a tree in breadth-first order.
    The first argument should be the tree root; children
    should be a function taking as argument a tree node and
    returning an iterator of the node's children.
    """
    yield tree
    last = tree
    for node in _breadth_first(tree, children):
        for child in children(node):
            yield child
            last = child

        if last == node:
            return


def suite_iter(suite):
    """suite_iter(suite) -> an iterator on its direct sub-suites.
    For compatibility with Python versions before 2.4"""

    def add_extra_description_field(test):
        test._testoob_extra_description = ''
        return True

    try:
        return _ifilter(add_extra_description_field, iter(suite))
    except TypeError:
        return _ifilter(add_extra_description_field, iter(suite._tests))


def full_extractor(suite, recursive_iterator=_breadth_first):
    """Extract the text fixtures from a suite.
    Descends recursively into sub-suites."""
    import unittest

    def test_children(node):
        if isinstance(node, unittest.TestSuite):
            return suite_iter(node)
        return []

    return _ifilter(lambda test: isinstance(test, unittest.TestCase), recursive_iterator(suite, children=test_children))


def _iterable_decorator(func):

    def decorator(extractor):

        def wrapper(*args, **kwargs):
            return func(extractor(*args, **kwargs))

        return wrapper

    return decorator


def predicate(pred):
    return _iterable_decorator(lambda iterable: _ifilter(pred, iterable))


def regex(regex):
    """Filter tests based on matching a regex to their id.
    Matching is performed with re.search"""
    import re
    compiled = re.compile(regex)

    def pred(test):
        return compiled.search(test.id())

    return predicate(pred)


def glob(pattern):
    """Filter tests based on a matching glob pattern to their id.
    Matching is performed with fnmatch.fnmatchcase"""
    import fnmatch

    def pred(test):
        return fnmatch.fnmatchcase(test.id(), pattern)

    return predicate(pred)


number_suffixes = {1: 'st', 2: 'nd', 3: 'ed'}

def _irepeat_items(num_times, iterable):
    for x in iterable:
        for i in xrange(num_times):
            try:
                x._testoob_extra_description = ' (%d%s iteration)' % (i + 1, number_suffixes.get(i + 1, 'th'))
            except (AttributeError, TypeError):
                pass

            yield x


def repeat(num_times):
    """Repeat each test a number of times"""
    return _iterable_decorator(lambda iterable: _irepeat_items(num_times, iterable))


def _irandomize(iterable, seed=None):
    """
    Randomize the iterable.

    Note: this evaluates the entire iterable to a sequence in memory, use
    this when this isn't an issue
    """
    if seed is None:
        from random import shuffle
    else:
        from random import Random
        shuffle = Random(seed).shuffle
    result = list(iterable)
    shuffle(result)
    return iter(result)
    return


def randomize(seed=None):
    """Randomize the order of the tests"""
    return _iterable_decorator(lambda iterable: _irandomize(iterable, seed))
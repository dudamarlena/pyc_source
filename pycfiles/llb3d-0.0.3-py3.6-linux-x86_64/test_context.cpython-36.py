# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/llb3d/tests/test_context.py
# Compiled at: 2019-01-14 10:34:00
# Size of source mod 2**32: 1509 bytes
"""Test case for backend."""
from pytest import raises
from ..context import Context, ContextProvider, current_context

def test_empty_context():
    """Check that context have functions and globals."""
    context = Context()
    if not context.functions == {}:
        raise AssertionError
    elif not context.globals == {}:
        raise AssertionError


def test_empty_context_provider():
    """Current context should be None by default."""
    with current_context() as (context):
        assert context is None


def test_simple_context_provider():
    """Check that context provider works with current_context proxy."""
    context = Context()
    with ContextProvider(context):
        with current_context() as (inner_context):
            assert inner_context is context


def test_exception():
    """Check that context provider throws exceptions."""
    context = Context()
    with raises(RuntimeError):
        with ContextProvider(context):
            with current_context():
                raise RuntimeError('simple error')


def test_recursive():
    """Check that context provider can be recursive."""
    context1 = Context()
    context2 = Context()
    with ContextProvider(context1):
        with current_context() as (inner_context1):
            assert context1 is inner_context1
        with ContextProvider(context2):
            with current_context() as (inner_context2):
                assert context2 is inner_context2
        with current_context() as (inner_context3):
            assert context1 is inner_context3
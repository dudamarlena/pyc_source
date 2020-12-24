# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nino/dev/marx/tests/workflow/test_context.py
# Compiled at: 2014-09-26 20:08:33
"""
Created on Feb 24, 2013

@author: nino
"""
import unittest
from marx.workflow.context import DefaultContext, Field
from marx.workflow.exceptions import InvalidContextAssignment
import nose.tools

class TestField(unittest.TestCase):

    def test1(self):

        class Context(DefaultContext):
            user = Field(int)
            str_or_float = Field(str, float)

        assert hasattr(Context, 'USER')
        assert Context.USER == 'user'
        assert hasattr(Context, 'user')
        c = Context(None)
        c.user = 1
        c.str_or_float = 's'
        c.str_or_float = 1.0
        assert c.user == 1
        with nose.tools.assert_raises(InvalidContextAssignment):
            c.user = 's'
        with nose.tools.assert_raises(InvalidContextAssignment):
            c.str_or_float = 1
        c2 = Context(None)
        assert c2.user is None
        return

    def test_contribute_to_class(self):
        pass

    def test_multiple_inheritance(self):

        class A(DefaultContext):
            a = Field(int)

        class B(DefaultContext):
            b = Field(str)

        class C(A, B):
            c = Field(int)

        c = C()
        for f in 'abc':
            assert hasattr(c, f)

        assert not hasattr(c, 'd')
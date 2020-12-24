# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nino/dev/marx/tests/workflow/test_flow.py
# Compiled at: 2014-09-26 20:08:33
"""
Created on Feb 23, 2013

@author: nino
"""
import unittest
from marx.workflow.flow import Workflow
from marx.workflow.exceptions import Abort, SkipStep
import nose.tools
from mock import Mock
from marx.workflow.context import DefaultContext

class TestAbort(unittest.TestCase):

    def abort_if_not_none(self, context):
        if self.x != None:
            raise Abort()
        return

    def skip(self, context):
        raise SkipStep()
        context.reply(1)

    def reply(self, context):
        context.reply(1)

    def assign(self, v):
        self.x = v

    def test_abort(self):
        self.x = None
        abort_if_not_none = self.abort_if_not_none
        assign = self.assign
        m = Mock()
        w = Workflow(steps=[abort_if_not_none, m])
        w(DefaultContext())
        assert m.called
        m.reset_mock()
        self.x = 1
        w = Workflow(steps=[abort_if_not_none, m])
        w(DefaultContext())
        assert not m.called
        m.reset_mock()
        self.x = None
        w = Workflow(steps=[abort_if_not_none,
         lambda context: assign(True),
         abort_if_not_none,
         m])
        w(DefaultContext())
        assert self.x is True
        assert not m.called
        return

    def test_custom_on_abort(self):
        m = Mock()
        m_a = Mock()
        self.x = 1
        w = Workflow(steps=[self.abort_if_not_none, m], on_abort=m_a)
        w(DefaultContext())
        assert not m.called
        assert m_a.called

    def test_reply_abort(self):
        self.x = None
        abort_if_not_none = self.abort_if_not_none
        assign = self.assign
        reply = self.reply
        self.x = None
        w = Workflow(steps=[abort_if_not_none, reply, reply,
         lambda context: assign(True),
         abort_if_not_none, reply])
        ctx = w(DefaultContext())
        assert ctx.replies == [1, 1]
        return

    def test_skip(self):
        w = Workflow(steps=[self.skip])
        ctx = w(DefaultContext())
        assert ctx.replies == []


class TestProgrammerError(unittest.TestCase):

    def test_bad_concatenation(self):
        with nose.tools.assert_raises(TypeError):
            Workflow() + 10


class TestOnError(unittest.TestCase):

    def test_default_on_error(self):
        m = Mock(side_effect=ValueError)
        w = Workflow(steps=[m])
        with nose.tools.assert_raises(ValueError):
            w(DefaultContext())

    def test_custom_on_error(self):
        m = Mock(side_effect=ValueError)
        m_f = Mock(return_value=1)
        w = Workflow(steps=[m], on_error=m_f)
        r = w(DefaultContext())
        assert m.called
        assert m_f.called
        assert r == 1
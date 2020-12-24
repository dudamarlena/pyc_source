# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/moser/code/pylint/pylint/test/unittest_checker_misc.py
# Compiled at: 2019-05-03 09:01:02
# Size of source mod 2**32: 3876 bytes
"""Tests for the misc checker."""
import builtins as @py_builtins, _pytest.assertion.rewrite as @pytest_ar
from pylint.checkers import misc
from pylint.testutils import CheckerTestCase, Message, _tokenize_str, set_config

class TestFixme(CheckerTestCase):
    CHECKER_CLASS = misc.EncodingChecker

    def test_fixme_with_message(self):
        code = 'a = 1\n                # FIXME message\n                '
        with self.assertAddsMessages(Message(msg_id='fixme', line=2, args='FIXME message')):
            self.checker.process_tokens(_tokenize_str(code))

    def test_todo_without_message(self):
        code = 'a = 1\n                # TODO\n                '
        with self.assertAddsMessages(Message(msg_id='fixme', line=2, args='TODO')):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_without_space(self):
        code = 'a = 1\n                #XXX\n                '
        with self.assertAddsMessages(Message(msg_id='fixme', line=2, args='XXX')):
            self.checker.process_tokens(_tokenize_str(code))

    def test_xxx_middle(self):
        code = 'a = 1\n                # midle XXX\n                '
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_without_space_fixme(self):
        code = 'a = 1\n                #FIXME\n                '
        with self.assertAddsMessages(Message(msg_id='fixme', line=2, args='FIXME')):
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=[])
    def test_absent_codetag(self):
        code = 'a = 1\n                # FIXME\t                # FIXME\n                # TODO\t                # TODO\n                # XXX\t                # XXX\n                '
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    @set_config(notes=['CODETAG'])
    def test_other_present_codetag(self):
        code = 'a = 1\n                # CODETAG\n                # FIXME\n                '
        with self.assertAddsMessages(Message(msg_id='fixme', line=2, args='CODETAG')):
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_not_trigger(self):
        code = 'print("# TODO this should not trigger a fixme")'
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))

    def test_issue_2321_should_trigger(self):
        code = '# TODO this should not trigger a fixme'
        with self.assertAddsMessages(Message(msg_id='fixme', line=1, args='TODO this should not trigger a fixme')):
            self.checker.process_tokens(_tokenize_str(code))

    def test_dont_trigger_on_todoist(self):
        code = '\n        # Todoist API: What is this task about?\n        # Todoist API: Look up a task\'s due date\n        # Todoist API: Look up a Project/Label/Task ID\n        # Todoist API: Fetch all labels\n        # Todoist API: "Name" value\n        # Todoist API: Get a task\'s priority\n        # Todoist API: Look up the Project ID a Task belongs to\n        # Todoist API: Fetch all Projects\n        # Todoist API: Fetch all Tasks\n        '
        with self.assertNoMessages():
            self.checker.process_tokens(_tokenize_str(code))
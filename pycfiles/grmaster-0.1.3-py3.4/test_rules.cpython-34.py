# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/tests/test_rules.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 2826 bytes
"""Tests for `grmaster.rules`."""
from grmaster import data
from grmaster.manager import Manager
from grmaster.rules import divide, add_english
STUDENTS_FILE = data.openfile('students.csv')

def test_divide():
    """Test internal function divide."""
    assert divide(50, 4) == [13, 13, 12, 12]
    assert divide(5, 6) == [1, 1, 1, 1, 1, 0]


class TestEnglishRule:
    __doc__ = 'Test case for `grmaster.rules`.'
    manager = None

    def setup(self):
        """Init data from test set."""
        STUDENTS_FILE.seek(0)
        self.manager = Manager(STUDENTS_FILE)
        assert len(self.manager.assign_chain) == 0
        assert len(self.manager.rule_chain) == 0
        add_english(self.manager)
        assert len(self.manager.rule_chain) == 1
        assert len(self.manager.assign_chain) == 1

    def test_english_rule_can_study(self):
        """Test that student can study in some groups. Not all."""
        student = self.manager.students[0]
        assert any(self.manager.can_study(student, group) for group in self.manager.group_ids)
        assert not all(self.manager.can_study(student, group) for group in self.manager.group_ids)

    def test_english_assign_student(self):
        """We can add student in some group."""
        student = self.manager.students[0]
        for group in self.manager.group_ids:
            if self.manager.can_study(student, group):
                if not self.manager.assign_student(student, group):
                    raise AssertionError
            elif not not self.manager.assign_student(student, group):
                raise AssertionError

    def test_english_assign_everybody(self):
        """We can add all students."""
        for student in self.manager.students:
            for group in self.manager.group_ids:
                if self.manager.can_study(student, group):
                    self.manager.assign_student(student, group)
                    break

        for student in self.manager.students:
            if not self.manager.is_assigned(student):
                raise AssertionError
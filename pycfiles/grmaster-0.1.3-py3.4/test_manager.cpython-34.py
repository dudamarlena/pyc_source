# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/tests/test_manager.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 2823 bytes
"""Tests for `grmaster.Manager`."""
from grmaster import data
from grmaster.manager import Manager, get_item, set_item

def test_get_item():
    """Full test."""
    arr = [
     [
      1, 2], [3, 4]]
    assert get_item(arr, [0, 0]) == 1
    assert get_item(arr, [0, 1]) == 2
    assert get_item(arr, [1, 0]) == 3
    assert get_item(arr, [1, 1]) == 4
    assert get_item(arr, [0]) == [1, 2]
    assert get_item(arr, [1]) == [3, 4]


def test_set_item():
    """Small test."""
    arr = [
     [
      1, 2], [3, 4]]
    set_item(arr, [0, 0], 5)
    assert arr == [[5, 2], [3, 4]]
    set_item(arr, [0, 1], 5)
    assert arr == [[5, 5], [3, 4]]
    set_item(arr, [1, 0], 5)
    assert arr == [[5, 5], [5, 4]]
    set_item(arr, [1, 1], 5)
    assert arr == [[5, 5], [5, 5]]


class TestManager:
    __doc__ = 'Tests for grmaster.Manager.'
    manager = None
    student = None

    def setup(self):
        """Just setup manager."""
        with data.openfile('students.csv') as (student_file):
            self.manager = Manager(student_file)
        assert isinstance(self.manager, Manager)
        self.student = self.manager.students[0]

    def test_manager_can_study(self):
        """Everybody can study everywhere."""
        assert all(self.manager.can_study(self.student, group) for group in self.manager.group_ids)

    def test_manager_assign_student(self):
        """Constant method."""
        self.manager.assign_student(self.student, [0, 0])
        assert self.manager.is_assigned(self.student)
        assert self.manager.result_groups[0] == [0, 0]

    def test_manager_is_assigned(self):
        """After assignation."""
        assert not self.manager.is_assigned(self.student)
        self.manager.assign_student(self.student, [0, 0])
        assert self.manager.is_assigned(self.student)

    def test_manager_assign_all(self):
        """We can assign everyone."""
        self.manager.assign_all()
        for student in self.manager.students:
            if not self.manager.is_assigned(student):
                raise AssertionError
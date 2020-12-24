# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/grmaster/manager.py
# Compiled at: 2015-05-28 11:03:40
# Size of source mod 2**32: 4106 bytes
"""Intermediate form of information about students and groups."""
from grmaster.table import Table, is_empty, next_or_empty
import csv

def set_item(container, indeces, value):
    """Set item in recursive list."""
    while len(indeces) > 1:
        container = container[indeces[0]]
        indeces = indeces[1:]

    container[indeces[0]] = value


def get_item(container, indeces):
    """Get item from recursive list."""
    while len(indeces) > 1:
        container = container[indeces[0]]
        indeces = indeces[1:]

    return container[indeces[0]]


class Manager:
    __doc__ = '\n    Manager is a list of streams.\n\n    Manager(csvfile).\n    '

    def __init__(self, students_file):
        """Initialize self.  See help(type(self)) for accurate signature."""
        self.config = {}
        self.meta = {}
        self.rule_chain = []
        self.assign_chain = []
        reader = csv.reader(students_file)
        finish_setup = False
        while not finish_setup:
            line = next(reader)
            if is_empty(line):
                finish_setup = True
            else:
                while line[(-1)] == '':
                    line = line[:-1]

                name = line[0].split('#')[0].strip()
                content = line[1:]
                self.config[name] = content

        self.stream_sizes = [int(x) for x in self.config['stream_sizes']]
        self.group_ids = [[stream, group] for stream in range(len(self.stream_sizes)) for group in range(self.stream_sizes[stream])]
        self.students = Table(reader)
        self.result_groups = [None for i in range(len(self.students))]
        name = next_or_empty(reader)
        while not is_empty(name):
            table = Table(reader)
            self.meta[name[0]] = table
            name = next_or_empty(reader)

    def can_study(self, student, group):
        """Functional part is in rule module. Just call it."""
        return all(rule(self, student, group) for rule in self.rule_chain)

    def assign_student(self, student, group):
        """Test and add."""
        if self.can_study(student, group):
            if all(add(self, student, group) for add in self.assign_chain):
                self.result_groups[self.students.body.index(student)] = group
                return True
        return False

    def is_assigned(self, student):
        """Return True, if student is assigned to some stream."""
        return self.result_groups[self.students.body.index(student)] is not None

    def assign_all(self):
        """Assign all students."""
        for student in self.students:
            if not self.is_assigned(student):
                for group in self.group_ids:
                    if self.assign_student(student, group):
                        break

                continue

    def group_name(self, group):
        """list -> str"""
        return str(100 + sum(self.stream_sizes[:group[0]]) + group[1] + 1)

    def get_result(self):
        """Write result_groups into students table."""
        students = [
         self.students.header + ('Group', )]
        for i in range(len(self.students)):
            students.append(self.students[i] + (
             self.group_name(self.result_groups[i]),))

        return Table(students)
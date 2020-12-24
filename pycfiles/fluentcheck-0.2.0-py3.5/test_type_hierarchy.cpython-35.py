# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_check/test_type_hierarchy.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 2227 bytes
import unittest
from fluentcheck.classes import Check
from fluentcheck.exceptions import CheckError

class ParentA:

    def __init__(self):
        pass


class Child(ParentA):

    def __init__(self):
        pass


class GrandChild(Child):

    def __init__(self):
        pass


class ParentB:

    def __init__(self):
        pass


class ChildOfMultipleParents(ParentA, ParentB):

    def __init__(self):
        pass


class TestTypeHierarchy(unittest.TestCase):

    def test_is_subtype_of(self):
        res = Check(Child()).is_subtype_of(ParentA)
        self.assertIsInstance(res, Check)
        try:
            Check(ParentA()).is_subtype_of(Child)
            self.fail()
        except CheckError:
            pass

    def test_is_subtype_of_when_grandchild_is_subtype_of_parent(self):
        res = Check(GrandChild()).is_subtype_of(ParentA)
        self.assertIsInstance(res, Check)
        try:
            Check(ParentA()).is_subtype_of(GrandChild)
            self.fail()
        except CheckError:
            pass

    def test_is_subtype_of_when_multiple_inheritance(self):
        res = Check(ChildOfMultipleParents()).is_subtype_of((ParentA, ParentB))
        self.assertIsInstance(res, Check)
        try:
            Check(ParentA()).is_subtype_of((ChildOfMultipleParents, ParentB))
            self.fail()
        except CheckError:
            pass

    def test_is_not_subtype_of(self):
        res = Check(ParentA()).is_not_subtype_of(ParentB)
        self.assertIsInstance(res, Check)
        try:
            Check(Child()).is_not_subtype_of(ParentA)
            self.fail()
        except CheckError:
            pass

    def test_is_subtype_of_itself(self):
        res = Check(Child()).is_subtype_of(Child)
        self.assertIsInstance(res, Check)
        try:
            Check(Child()).is_not_subtype_of(Child)
            self.fail()
        except CheckError:
            pass

    def test_is_subtype_of_atleast_one_parent(self):
        res = Check(Child()).is_subtype_of((ParentA, ParentB))
        self.assertIsInstance(res, Check)
        try:
            Check(Child()).is_not_subtype_of((ParentA, ParentB))
            self.fail()
        except CheckError:
            pass
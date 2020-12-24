# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/soktest/base.py
# Compiled at: 2013-12-20 07:25:46
# Size of source mod 2**32: 2991 bytes
import unittest
from soktest.error import NameAlreadyExists
from mock import patch
from six import add_metaclass

class TestCaseType(type):

    @classmethod
    def assign_groups(cls, test):
        for group in test.groups:
            if group not in TestCase._alltests_groups:
                TestCase._alltests_groups[group] = []
            TestCase._alltests_groups[group].append(test)

    @classmethod
    def validate_name(cls, fullname):
        keys = TestCase._alltests_dict.keys()
        if fullname in keys:
            raise NameAlreadyExists(fullname)

    @classmethod
    def add_test_to_alltests(cls, name, test):
        keys = TestCase._alltests_dict.keys()
        if name in keys:
            TestCase._alltests_dict[name] = None
        else:
            TestCase._alltests_dict[name] = test

    @classmethod
    def get_full_name(cls, dct, name):
        return '.'.join([str(dct['__module__']), name])

    @classmethod
    def init_task(cls, task, name, dct):
        fullname = cls.get_full_name(dct, name)
        if 'base' not in dct or dct['base'] == False:
            cls.validate_name(fullname)
            cls.add_test_to_alltests(name, task)
            cls.assign_groups(task)
            TestCase._alltests_dict[fullname] = task
            TestCase._alltests.append(task)

    def __init__(cls, name, bases, dct):
        super(TestCaseType, cls).__init__(name, bases, dct)
        TestCaseType.init_task(cls, name, dct)


@add_metaclass(TestCaseType)
class TestCase(unittest.TestCase):
    _alltests = []
    _alltests_dict = {}
    _alltests_groups = {}
    base = True
    groups = ('unit', )

    def _init_patchers(self):
        pass

    def _start_patchers(self):
        for name, patcher in self.patchers.items():
            self.mocks[name] = patcher.start()

    def _stop_patchers(self):
        for name, patcher in self.patchers.items():
            try:
                patcher.stop()
            except AttributeError:
                pass

    def _add_patcher(self, name, patcher):
        self.patchers[name] = patcher
        self.mocks[name] = patcher.start()

    def add_mock(self, url, *args, **kwargs):
        name = url.split('.')[(-1)]
        patcher = patch(url, *args, **kwargs)
        self._add_patcher(name, patcher)

    def add_mock_object(self, obj, name, *args, **kwargs):
        patcher = patch.object(obj, name, *args, **kwargs)
        self._add_patcher(name, patcher)

    def _setUpPatchers(self):
        self.patchers = {}
        self.mocks = {}
        self._init_patchers()
        self._start_patchers()

    def setUp(self):
        super(TestCase, self).setUp()
        self._setUpPatchers()

    def tearDown(self):
        super(TestCase, self).tearDown()
        self._stop_patchers()
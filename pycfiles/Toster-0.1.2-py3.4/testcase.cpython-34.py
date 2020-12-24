# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toster/testcase.py
# Compiled at: 2014-08-25 15:54:39
# Size of source mod 2**32: 1603 bytes
import unittest
from mock import patch

class TestCase(unittest.TestCase):
    groups = ('unit', )
    prefix_from = None
    prefix = ''

    def setUp(self):
        super().setUp()
        self._setUpPatchers()

    def _setUpPatchers(self):
        self.patchers = {}
        self.mocks = {}
        self.init_patchers()
        self._start_patchers()

    def init_patchers(self):
        pass

    def _start_patchers(self):
        for name, patcher in self.patchers.items():
            self.mocks[name] = patcher.start()

    def tearDown(self):
        super().tearDown()
        self._stop_patchers()

    def _stop_patchers(self):
        for name, patcher in self.patchers.items():
            try:
                patcher.stop()
            except AttributeError:
                pass

    def _add_patcher(self, name, patcher):
        self.patchers[name] = patcher
        self.mocks[name] = patcher.start()

    def add_mock(self, url, prefix=None, *args, **kwargs):
        prefix = prefix or self.get_prefix()
        full_url = prefix + url
        name = full_url.split('.')[(-1)]
        patcher = patch(full_url, *args, **kwargs)
        self._add_patcher(name, patcher)

    def get_prefix(self):
        if self.prefix_from is None:
            return self.prefix
        else:
            return self.prefix_from.__module__ + '.'

    def add_mock_object(self, obj, name, *args, **kwargs):
        patcher = patch.object(obj, name, *args, **kwargs)
        self._add_patcher(name, patcher)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/example/venv_impex/lib/python3.5/site-packages/impaf/tests/test_utils.py
# Compiled at: 2015-06-26 14:26:13
# Size of source mod 2**32: 378 bytes
from ..utils import cached

class ExampleCached(object):

    def __init__(self):
        self._cache = {}
        self.runned = 0

    @cached
    def counting(self):
        self.runned += 1
        return self.runned


class TestCached(object):

    def test_simple(self):
        obj = ExampleCached()
        assert obj.counting() == 1
        assert obj.counting() == 1
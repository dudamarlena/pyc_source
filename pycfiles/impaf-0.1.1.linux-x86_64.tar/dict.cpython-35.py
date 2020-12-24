# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/socek/projects/impaf/core/build/lib/impaf/testing/dict.py
# Compiled at: 2015-08-04 15:30:38
# Size of source mod 2**32: 245 bytes
from mock import MagicMock

class MockedDict(dict):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._mock = MagicMock()

    def __getattr__(self, name):
        return getattr(self._mock, name)
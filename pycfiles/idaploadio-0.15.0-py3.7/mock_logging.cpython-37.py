# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/idapload/test/mock_logging.py
# Compiled at: 2020-04-13 02:37:12
# Size of source mod 2**32: 398 bytes
import logging

class MockedLoggingHandler(logging.Handler):
    debug = []
    warning = []
    info = []
    error = []

    def emit(self, record):
        getattr(self.__class__, record.levelname.lower()).append(record.getMessage())

    @classmethod
    def reset(cls):
        for attr in dir(cls):
            if isinstance(getattr(cls, attr), list):
                setattr(cls, attr, [])
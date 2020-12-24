# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/tests/util/mockedio.py
# Compiled at: 2015-11-06 23:45:35
import mock
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

class MockedIO(object):

    def __init__(self):
        self.stderr = StringIO()
        self.stdout = StringIO()
        self.stderr_patch = mock.patch('sys.stderr', self.stderr)
        self.stdout_patch = mock.patch('sys.stdout', self.stdout)

    def setUp(self):
        self.stderr_patch.start()
        self.stdout_patch.start()

    def tearDown(self):
        self.stderr_patch.stop()
        self.stdout_patch.stop()
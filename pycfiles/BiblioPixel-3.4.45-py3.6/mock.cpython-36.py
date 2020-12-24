# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/bibliopixel/mock.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 901 bytes
from argparse import Namespace
from . import patch

class MockFP(object):

    def __init__(self, filename, filesystem):
        self.filename = filename
        self.filesystem = filesystem
        self.write_started = False

    def read(self):
        return self.filesystem[self.filename]

    def write(self, x):
        if self.write_started:
            self.filesystem[self.filename] += x
        else:
            self.write_started = True
            self.filesystem[self.filename] = x

    def __iter__(self):
        return iter(self.read().splitlines())

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        pass


def mock_open(filesystem):

    def open(filename, access='r'):
        return MockFP(filename, filesystem)

    return open


def patch_open(filesystem, object):
    return patch.patch(object, 'open', mock_open(filesystem))
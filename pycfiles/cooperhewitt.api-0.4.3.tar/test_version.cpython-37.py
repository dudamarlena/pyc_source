# uncompyle6 version 3.6.7
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cooperative/tests/test_version.py
# Compiled at: 2015-05-25 03:34:59
# Size of source mod 2**32: 418 bytes
import unittest

class TestMeta(unittest.TestCase):

    def test_version_defined(self):
        """
        Ensure __version__ is defined in the stream_tap module.

        Ensure __version_info__ is defined in the stream_tap module.

        """
        from stream_tap import __version__
        from stream_tap import __version_info__
        self.assertTrue(__version__)
        self.assertTrue(__version_info__)
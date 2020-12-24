# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bd2k/util/test/test_files.py
# Compiled at: 2018-05-03 13:55:55
from builtins import range
from unittest import TestCase
from mock import MagicMock, call

class TestFiles(TestCase):
    if False:
        from bd2k.util.files import gread, gwrite

        def test_gread(self):
            for n in range(0, 4):
                f = MagicMock()
                f.read.side_effect = [
                 '1', '2', '']
                self.assertEqual(self.gread(f, n), '12'[:n])
                self.assertEqual(f.mock_calls, [ call.read(i) for i in range(n, 0, -1) ])

        def test_gwrite(self):
            for n in range(0, 3):
                f = MagicMock()
                f.write.side_effect = [
                 1] * n
                s = '12'[:n]
                self.gwrite(f, s)
                self.assertEqual(f.mock_calls, [ call.write(s[i:]) for i in range(0, n) ])
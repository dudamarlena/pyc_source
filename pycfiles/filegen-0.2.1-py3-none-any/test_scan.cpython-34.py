# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/nao/vboxshare/venvs/django/filegen/filegen/tests/test_scan.py
# Compiled at: 2016-05-21 05:47:07
# Size of source mod 2**32: 599 bytes
import unittest
from evilunit import test_target

@test_target('filegen.scanning:MakoTemplateScanner')
class Tests(unittest.TestCase):

    def _makeOne(self):
        from filegen.scanning import ScannerContext
        return self._getTarget()(ScannerContext())

    def test_it(self):
        C = self._makeOne()
        template = '\n        <% two = 1 + 1%>\n        ${two}\n        ${two + 2}\n        ${two + three * 3}\n        ${not one}\n        ${four("xxx", five)}\n        '
        result = C.scan(template)
        self.assertEqual(list(sorted(result)), ['five', 'one', 'three', 'two'])
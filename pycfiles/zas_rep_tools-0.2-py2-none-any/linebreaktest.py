# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/linebreaktest.py
# Compiled at: 2018-07-23 18:20:27
from __future__ import absolute_import, division, print_function, unicode_literals
import doctest, unittest
from . import linebreak
from .db import iter_line_break_tests
from .test import implement_break_tests
skips = [
 (
  b'}$', [1, 2]),
 (
  b'$(', [1, 2]),
 (
  b'$(', [1, 2]),
 (
  b'$̈(', [2, 3]),
 (
  b'%(', [1, 2]),
 (
  b'%̈(', [2, 3]),
 (
  b')$', [1, 2]),
 (
  b')%', [1, 2]),
 (
  b')̈$', [2, 3]),
 (
  b')̈%', [2, 3]),
 (
  b',0', [1, 2]),
 (
  b',̈0', [2, 3]),
 (
  b'/0', [1, 2]),
 (
  b'/̈0', [2, 3]),
 (
  b'봐요. A.3 못', [1, 4, 6, 8, 9]),
 (
  b'봤어. A.2 볼', [1, 4, 6, 8, 9]),
 (
  b'요. A.4 못', [3, 5, 7, 8]),
 (
  b'A.1 못', [2, 4, 5]),
 (
  b'a.2 ', [2, 4]),
 (
  b'a.2 क', [2, 4, 5]),
 (
  b'a.2 本', [2, 4, 5]),
 (
  b'a.2\u30003', [2, 3, 4, 5]),
 (
  b'a.2\u30003', [2, 3, 4, 5]),
 (
  b'a.2\u3000「', [2, 3, 4, 5]),
 (
  b'a.2\u3000ま', [2, 3, 4, 5]),
 (
  b'a.2\u3000本', [2, 3, 4, 5]),
 (
  b'code\\(s\\)', [4, 5, 7, 9]),
 (
  b'code\\{s\\}', [4, 5, 7, 9]),
 (
  b'equals .35 cents', [8, 11, 16]),
 (
  b'}%', [1, 2]),
 (
  b'}̈$', [2, 3]),
 (
  b'}̈%', [2, 3])]

@implement_break_tests(linebreak.line_break_boundaries, iter_line_break_tests(), skips)
class LineBreakTest(unittest.TestCase):
    pass


def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(linebreak))
    return tests


if __name__ == b'__main__':
    unittest.main()
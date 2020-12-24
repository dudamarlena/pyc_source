# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /private/var/folders/_d/md744_dn7ggffch8955xb93h0000gs/T/pip-install-xY4LYQ/uniseg/uniseg/wraptest.py
# Compiled at: 2018-07-23 18:20:27
from __future__ import absolute_import, division, print_function, unicode_literals
import doctest, unittest
from . import wrap

def load_tests(loader, tests, ignore):
    tests.addTests(doctest.DocTestSuite(wrap))
    return tests


if __name__ == b'__main__':
    unittest.main()
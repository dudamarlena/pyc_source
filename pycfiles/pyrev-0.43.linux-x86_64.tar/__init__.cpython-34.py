# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/griflet/venv/lib/python3.4/site-packages/test/__init__.py
# Compiled at: 2017-02-20 22:32:52
# Size of source mod 2**32: 453 bytes
from __future__ import absolute_import
import unittest
from .regtest import RegressionTest
from .parsertest import ParserTest
from .projecttest import ProjectTest
__all__ = [
 'RegressionTest', 'ParserTest', 'ProjectTest']
if __name__ == '__main__':
    unittest.main()
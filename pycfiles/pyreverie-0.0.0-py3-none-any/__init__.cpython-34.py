# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
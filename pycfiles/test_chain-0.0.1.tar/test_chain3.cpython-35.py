# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\github\testchain\test_chain\test_chain3.py
# Compiled at: 2017-01-04 10:26:59
# Size of source mod 2**32: 381 bytes
from .test_chain_meta import TestChainMeta
import unittest

class TestChain(unittest.TestCase, metaclass=TestChainMeta):
    __doc__ = '\n    Creates an instance of a testChain class for easy implementation through extension\n    This particular instance is created in the syntax of Python 3.5 to account for slight\n    variations in the use of metaclasses between versions\n    '
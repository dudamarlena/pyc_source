# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fluentcheck/tests/tests_is/test_chain_closure_is.py
# Compiled at: 2020-04-04 09:18:50
# Size of source mod 2**32: 355 bytes
import unittest
from fluentcheck import Is

class TestIsChainClosure(unittest.TestCase):

    def test_chain_closure_with(self):
        Is(0.5).not_none.number.truthy()

    def test_chain_closure_without(self):
        Is(0.5).not_none.number.truthy
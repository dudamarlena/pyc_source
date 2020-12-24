# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/corykitchens/Workspace/learn_cli/venv/lib/python3.6/site-packages/tests/test_cfn.py
# Compiled at: 2019-04-22 19:33:35
# Size of source mod 2**32: 460 bytes
from unittest import TestCase
from unittest.mock import MagicMock, patch
from logging import getLogger, DEBUG
from cfn import say_hello
logger = getLogger(__name__)
logger.setLevel(DEBUG)

class TestCfn(TestCase):

    def setUp(self):
        logger.debug('Inside setup')

    def test_say_hello_returns_hello_world(self):
        expected = 'Hello World'
        received = say_hello()
        self.assertEqual(expected, received, f"Expected {expected} Received {received}")
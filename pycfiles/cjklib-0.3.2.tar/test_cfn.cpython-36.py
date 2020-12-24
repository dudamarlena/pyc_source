# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
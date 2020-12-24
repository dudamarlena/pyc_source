# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/tests/test_basecontroller.py
# Compiled at: 2010-10-30 02:42:53
from unittest import TestCase
import logging
log = logging.getLogger(__name__)
from nose.tools import *
from aha.controller.basecontroller import BaseController

class TestBaseController(TestCase):

    def test_controller(self):
        """
        Test for authenticate decorator
        """
        pass
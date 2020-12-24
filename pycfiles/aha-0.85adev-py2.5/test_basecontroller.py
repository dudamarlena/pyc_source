# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
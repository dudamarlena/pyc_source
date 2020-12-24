# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-i386/egg/djangoflash/tests/context_processors.py
# Compiled at: 2011-01-28 16:01:34
"""djangoflash.context_processors test cases.
"""
from unittest import TestCase
from django.core.exceptions import SuspiciousOperation
from django.http import HttpRequest
from djangoflash.context_processors import CONTEXT_VAR, flash
from djangoflash.models import FlashScope

class FlashContextProcessorTestCase(TestCase):
    """Tests the context processor used to expose the flash to view templates.
    """

    def setUp(self):
        self.request = HttpRequest()
        self.scope = FlashScope()
        setattr(self.request, CONTEXT_VAR, self.scope)

    def test_expose_flash(self):
        """FlashContextProcessor: should expose the flash to view templates.
        """
        self.assertEqual(flash(self.request), {CONTEXT_VAR: self.scope})

    def test_expose_inexistent_flash(self):
        """FlashContextProcessor: should fail when there's no flash available.
        """
        delattr(self.request, CONTEXT_VAR)
        self.assertTrue(isinstance(flash(self.request)[CONTEXT_VAR], FlashScope))

    def test_expose_invalid_flash(self):
        """FlashContextProcessor: should fail when exposing an invalid object as being the flash.
        """
        self.request.flash = 'Invalid object'
        self.assertRaises(SuspiciousOperation, flash, self.request)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/tests/__init__.py
# Compiled at: 2009-03-12 14:14:57
"""
Test suite for the repoze.what Pylons plugin.

This module includes miscellaneous tests.

"""
from inspect import ismethod
from unittest import TestCase
from repoze.what.plugins.pylonshq import ControllerProtector

class TestControllerDecorator(TestCase):
    """Framework-independent tests for @ControllerProtector decorator"""

    def test_controller_class(self):
        """The ``__before__`` method must be defined if passed a class"""

        class DaController(object):
            pass

        DaController = ControllerProtector(None)(DaController)
        assert hasattr(DaController, '__before__')
        assert ismethod(DaController.__before__)
        return

    def test_controller_instance(self):
        """
        The ``__before__`` method must be defined if passed a class
        instance.
        
        """

        class DaController(object):
            pass

        da_instance = DaController()
        da_instance = ControllerProtector(None)(da_instance)
        assert hasattr(da_instance, '__before__')
        assert ismethod(da_instance.__before__)
        return
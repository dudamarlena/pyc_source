# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/aha/controller/tests/test_controller.py
# Compiled at: 2010-10-20 22:45:56
from unittest import TestCase
import logging
log = logging.getLogger(__name__)
from nose.tools import *
from coregae.controller.formcontrol import FormControl, handle_state, validate
FC = FormControl

class TestCRUDControllerMixIn(TestCase):

    def test_subclass(self):
        """
        Test for subclassing CRUDControllerMixIn
        """
        from coregae.controller.crudcontrollers import CRUDControllerMixIn, CRUDControllerMetaClass

        class TestKlass(CRUDControllerMixIn):
            EDIT_FC = FormControl()
            ADD_FC = FormControl()

            @EDIT_FC.handle_state(FC.SUCCESS)
            def edit_data(self):
                return 'FOO'

            @EDIT_FC.handle_validate(FC.INITIAL)
            def edit_validate(self):
                pass

            @ADD_FC.handle_state(FC.INITIAL)
            def add_form(self):
                return 'FOO'

        assert_true(hasattr(TestKlass, 'EDIT_FC'))
        assert_true(hasattr(TestKlass, 'ADD_FC'))
        assert_not_equal(TestKlass.EDIT_FC, CRUDControllerMixIn.EDIT_FC)
        efc = TestKlass.EDIT_FC
        efc2 = CRUDControllerMixIn.EDIT_FC
        assert_equal(efc.get_processor(FC.INITIAL), efc2.get_processor(FC.INITIAL))
        assert_not_equal(efc.get_processor(FC.SUCCESS), efc2.get_processor(FC.SUCCESS))
        assert_not_equal(efc.get_validator(FC.INITIAL), efc2.get_validator(FC.INITIAL))
        afc = TestKlass.ADD_FC
        afc2 = CRUDControllerMixIn.ADD_FC
        assert_not_equal(afc.get_processor(FC.INITIAL), afc2.get_processor(FC.INITIAL))
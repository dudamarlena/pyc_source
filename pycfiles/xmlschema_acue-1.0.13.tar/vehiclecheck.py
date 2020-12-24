# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /local/hd1/home1/data/acue/rd/p-open-deploy/xmlschema_acue/components/xmlschema_acue/testdata/xmlschema_acue_testdata/examples/vehicles/vehiclecheck.py
# Compiled at: 2019-05-19 13:15:11
from xmlschema_acue.validators import ModelVisitor
from tests.xmlschema_acue_tests.testtools.TestCaseXMLSchema import XMLSchemaTestCase

class VehiclesBase(XMLSchemaTestCase):

    def check_advance_true(self, model, expected=None):
        """
        Advances a model with a match condition and checks the expected error list or exception.

        :param model: an ModelGroupVisitor instance.
        :param expected: can be an exception class or a list. Leaving `None` means that an empty         list is expected.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            self.assertRaises(expected, lambda x: list(model.advance(x)), True)
        else:
            self.assertEqual([ e for e in model.advance(True) ], expected or [])

    def check_advance_false(self, model, expected=None):
        """
        Advances a model with a no-match condition and checks the expected error list or  or exception.

        :param model: an ModelGroupVisitor instance.
        :param expected: can be an exception class or a list. Leaving `None` means that an empty         list is expected.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            self.assertRaises(expected, lambda x: list(model.advance(x)), False)
        else:
            self.assertEqual([ e for e in model.advance(False) ], expected or [])

    def check_advance(self, model, match, expected=None):
        """
        Advances a model with an argument match condition and checks the expected error list.

        :param model: an ModelGroupVisitor instance.
        :param match: the matching boolean condition.
        :param expected: can be an exception class or a list. Leaving `None` means that an empty         list is expected.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            self.assertRaises(expected, lambda x: list(model.advance(x)), match)
        else:
            self.assertEqual([ e for e in model.advance(match) ], expected or [])

    def check_stop(self, model, expected=None):
        """
        Stops a model and checks the expected errors list.

        :param model: an ModelGroupVisitor instance.
        :param expected: can be an exception class or a list. Leaving `None` means that an empty         list is expected.
        """
        if isinstance(expected, type) and issubclass(expected, Exception):
            self.assertRaises(expected, lambda : list(model.stop()))
        else:
            self.assertEqual([ e for e in model.stop() ], expected or [])
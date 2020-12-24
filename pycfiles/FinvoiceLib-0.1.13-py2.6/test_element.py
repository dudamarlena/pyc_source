# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/tests/elements/test_element.py
# Compiled at: 2010-03-24 05:43:08
from finvoicelib.elements import Element
from finvoicelib.tests import FinvoiceTestCase

class TestElement(FinvoiceTestCase):

    def test_init_with_none(self):
        """
        Test finvoice.elements.Element.__init__ with tag=None
        """
        e = Element(None)
        self.assertEqual(e.tag, None)
        return

    def test_init_with_tag(self):
        """
        Test finvoice.elements.Element.__init__ with tag='SomeElement'
        """
        e = Element('SomeElement')
        self.assertEqual(e.tag, 'SomeElement')


class TestElementSubclassing(FinvoiceTestCase):

    def setUp(self):

        class ChildElement(Element):
            tag = 'ChildElement'

        class SomeElement(Element):
            tag = 'SomeElement'
            aggregate = [ChildElement]

            def set_attributes(self):
                self.attributes = {'my_attr': None}
                return

        self.some_element = SomeElement()

    def test_supported_elements(self):
        s = self.some_element
        self.assertEqual(s.supported_elements, ['ChildElement'])

    def test_attributes(self):
        s = self.some_element
        self.assertEqual(s.my_attr, None)
        return

    def test_has_mapping_for(self):
        s = self.some_element
        self.failUnless(s.has_mapping_for('ChildElement'))
        self.failIf(s.has_mapping_for('UnknownElement'))
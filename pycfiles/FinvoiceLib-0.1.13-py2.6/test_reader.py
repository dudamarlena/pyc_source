# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/finvoicelib/tests/reader/test_reader.py
# Compiled at: 2010-03-24 05:43:08
from StringIO import StringIO
from finvoicelib.reader.finvoice_reader import Reader
from finvoicelib.tests import FinvoiceTestCase

class TestReader(FinvoiceTestCase):
    document = None

    def test_init_with_pulli(self):
        """
        Test finvoice.reader.Reader.__init__ with "Pulli" finvoice
        """
        reader = Reader(self.get_pulli_finvoice())
        self.failUnless(len(reader.messages) == 1)

    def test_init_with_pankkiyhdistys_finvoice(self):
        """
        Test finvoice.reader.Reader.__init__ with "pankkiyhdistys" finvoice
        """
        reader = Reader(self.get_pankkiyhdistys_finvoice())
        self.failUnless(len(reader.messages) == 1)

    def test_init_with_combined_finvoice(self):
        """
        Test finvoice.reader.Reader.__init__ a combined finvoice

        """
        pulli_data = self.get_pulli_finvoice().read()
        pankkiyhdistys_data = self.get_pankkiyhdistys_finvoice().read()
        data = pulli_data + '\n' + pankkiyhdistys_data
        f = StringIO(data)
        reader = Reader(f)
        self.failUnless(len(reader.messages) == 2)
        self.assertEqual(reader.messages[0].envelope_tree, None)
        self.assertNotEqual(reader.messages[1].envelope_tree, None)
        return
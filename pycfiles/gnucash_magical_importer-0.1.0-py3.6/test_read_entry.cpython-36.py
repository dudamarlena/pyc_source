# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/test/test_read_entry.py
# Compiled at: 2018-12-13 21:04:34
# Size of source mod 2**32: 597 bytes
from gnucash_importer.read_entry import OfxReader, QifReader, CsvReader
from gnucash_importer.util import Util
import unittest

class EntryReaderTestCase(unittest.TestCase):

    def test_get_transactions_ofx(self):
        transactions = OfxReader().get_transactions(Util().DEFAULT_ACCOUNT_SRC_FILE)
        self.assertEqual(len(transactions), 9)

    @unittest.skip('not implemented yet')
    def test_get_transactions_qif(self):
        pass

    @unittest.skip('not implemented yet')
    def test_get_transactions_csv(self):
        pass


if __name__ == '__main__':
    unittest.main()
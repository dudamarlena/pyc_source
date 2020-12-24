# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gnucash_importer/read_entry.py
# Compiled at: 2018-11-28 19:46:12
# Size of source mod 2**32: 2262 bytes
"""Module to read all file formats that will be supported."""
from abc import abstractmethod
import logging
from ofxparse import OfxParser

class EntryReader(object):
    __doc__ = 'Aggreates all functions and act as interface.'
    transactions = None

    def __init__(self):
        pass

    @abstractmethod
    def get_transaction(self, report_file):
        """Given a file, get all transactions there."""
        pass

    def print_transactions(self):
        """Print to standard output all transactions stored in this class. Require get_transaction before use this method."""
        for transaction in self.transactions:
            self.print_transaction(transaction)

    def print_transaction(self, transaction):
        """Print to standard output one transaction at time."""
        print('+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++')
        print('amount....: %s' % transaction.amount)
        print('checknum..: %s' % transaction.checknum)
        print('date......: %s' % transaction.date)
        print('id........: %s' % transaction.id)
        print('mcc.......: %s' % transaction.mcc)
        print('memo......: %s' % transaction.memo.encode('iso-8859-1'))
        print('payee.....: %s' % transaction.payee)
        print('sic.......: %s' % transaction.sic)
        print('type......: %s' % transaction.type)


class OfxReader(EntryReader):
    __doc__ = 'Implement EntryReader class specialized in OFX data file.'

    def get_transactions(self, report_file):
        """Implement super behavior."""
        report = open(report_file)
        ofx = OfxParser.parse(report)
        self.transactions = ofx.account.statement.transactions
        report.close()
        return self.transactions


class QifReader(EntryReader):
    __doc__ = 'Implement EntryReader class specialized in QIF data file.'

    def get_transactions(self, report_file):
        """TODO STUB METHOD. Implement super behavior."""
        print('TODO STUB METHOD.')


class CsvReader(EntryReader):
    __doc__ = 'Implement EntryReader class specialized in CSV data file.'

    def get_transactions(self, report_file):
        """TODO STUB METHOD. Implement super behavior."""
        print('TODO STUB METHOD.')
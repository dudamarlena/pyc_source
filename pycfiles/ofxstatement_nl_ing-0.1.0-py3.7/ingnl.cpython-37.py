# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ofxstatement/plugins/ingnl.py
# Compiled at: 2019-11-17 09:03:30
# Size of source mod 2**32: 1666 bytes
import csv
from ofxstatement import statement
from ofxstatement.plugin import Plugin
from ofxstatement.parser import CsvStatementParser
from ofxstatement.parser import StatementParser
from ofxstatement.statement import StatementLine

class IngNlPlugin(Plugin):
    __doc__ = 'ING Netherlands Plugin\n    '

    def get_parser(self, filename):
        f = open(filename, 'r', encoding=(self.settings.get('charset', 'UTF-8')))
        return IngNlParser(f)


class IngNlParser(CsvStatementParser):
    date_format = '%Y%m%d'
    mappings = {'date':0, 
     'payee':1, 
     'trntype':5, 
     'amount':6, 
     'memo':8}

    def parse(self):
        stmt = super().parse()
        stmt.account_id = self.acct
        stmt.bank_id = None
        stmt.currency = 'EUR'
        statement.recalculate_balance(stmt)
        return stmt

    def split_records(self):
        """Return iterable object consisting of a line per transaction
        """
        reader = csv.reader((self.fin), delimiter=',', quotechar='"')
        next(reader, None)
        return reader

    def parse_record(self, line):
        if line[5] in ('Af', 'Debit'):
            line[5] = 'DEBIT'
        else:
            if line[5] in ('Bij', 'Credit'):
                line[5] = 'CREDIT'
        line[6] = line[6].replace(',', '.')
        self.acct = line[2]
        return super().parse_record(line)
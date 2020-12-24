# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bdgt/importer/parsers.py
# Compiled at: 2014-10-31 03:15:09
from __future__ import absolute_import
import datetime, csv, os, re, tempfile
from mt940 import MT940
from ofxparse import OfxParser as OfxLibParser
from bdgt.importer.types import ImportTx, ParsedTx

class TxParserFactory(object):

    @classmethod
    def create(cls, type_):
        if type_ == 'csv-ing':
            return CsvIngParser()
        if type_ == 'mt940':
            return Mt940Parser()
        if type_ == 'ofx':
            return OfxParser()
        raise ValueError(("Unknown parser type '{}'").format(type_))


class Mt940Parser(object):

    def parse(self, file_):
        mt940 = MT940(file_)
        i_txs = []
        for f_stmt in mt940.statements:
            for f_tx in f_stmt.transactions:
                p_tx = ParsedTx(f_tx.booking, f_tx.amount, unicode(f_tx.account), unicode(f_tx.description))
                i_tx = ImportTx(p_tx)
                i_txs.append(i_tx)

        return i_txs


class OfxParser(object):

    def parse(self, file_):
        with open(file_) as (f):
            data = f.read()
        data = re.sub('<TRNAMT>([-\\d]+),([\\d]+)', '<TRNAMT>\\1.\\2', data)
        ofx_file = tempfile.NamedTemporaryFile(delete=False)
        try:
            with ofx_file as (f):
                f.write(data)
            ofx = OfxLibParser.parse(file(ofx_file.name))
            i_txs = []
            for f_acc in ofx.accounts:
                for f_tx in f_acc.statement.transactions:
                    p_tx = ParsedTx(f_tx.date.date(), f_tx.amount, unicode(f_acc.number), unicode(f_tx.memo))
                    i_tx = ImportTx(p_tx)
                    i_txs.append(i_tx)

            return i_txs
        finally:
            os.remove(ofx_file.name)


class CsvIngParser(object):

    def parse(self, file_):
        if not os.path.exists(file_):
            raise ValueError(("'{}' not found").format(file_))
        with open(file_, 'r') as (f):
            csv_reader = csv.DictReader(f)
            i_txs = []
            for tx in csv_reader:
                if '-' in tx['Datum']:
                    fmt = '%d-%m-%Y'
                else:
                    fmt = '%Y%m%d'
                tx_date = datetime.datetime.strptime(tx['Datum'], fmt).date()
                try:
                    tx_amount = float(tx['Bedrag (EUR)'])
                except ValueError:
                    tx_amount = float(tx['Bedrag (EUR)'].replace(',', '.'))

                if tx['Af Bij'] == 'Af':
                    tx_amount = -tx_amount
                tx_account = unicode(tx['Rekening'])
                tx_description = unicode(tx['Naam / Omschrijving'])
                tx_description += '\n' + unicode(tx['Mededelingen'])
                p_tx = ParsedTx(tx_date, tx_amount, tx_account, tx_description)
                i_tx = ImportTx(p_tx)
                i_txs.append(i_tx)

            return i_txs
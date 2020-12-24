# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_import_parser_csv_ing.py
# Compiled at: 2014-10-31 03:15:09
import datetime, os, tempfile
from mock import patch
from nose.tools import eq_, ok_
from bdgt.importer.parsers import CsvIngParser

@patch('os.path.exists', return_value=True)
def test_parse(mock_exists):
    txs_data = '"Datum","Naam / Omschrijving","Rekening","Tegenrekening","Code","Af Bij","Bedrag (EUR)","MutatieSoort","Mededelingen"\n' + '"20150801","Naam en omsch.","987654321","11112222","BA","Af","12,75","Betaalautomaat","Mededelingen hier"\n' + '"20150802","Naam en omsch.","987654321","12321232","GT","Bij","8,50","Internetbankieren","Mededelingen hier"'
    data_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with data_file as (f):
            f.write(txs_data)
        parser = CsvIngParser()
        txs = parser.parse(data_file.name)
        eq_(len(txs), 2)
        eq_(txs[0]._parsed_tx.date, datetime.date(2015, 8, 1))
        eq_(txs[0]._parsed_tx.amount, -12.75)
        eq_(txs[0]._parsed_tx.account, '987654321')
        eq_(txs[0]._parsed_tx.description, 'Naam en omsch.\nMededelingen hier')
        eq_(txs[1]._parsed_tx.date, datetime.date(2015, 8, 2))
        eq_(txs[1]._parsed_tx.amount, 8.5)
        eq_(txs[1]._parsed_tx.account, '987654321')
        eq_(txs[1]._parsed_tx.description, 'Naam en omsch.\nMededelingen hier')
        ok_(type(txs[0]._parsed_tx.account) == unicode)
        ok_(type(txs[0]._parsed_tx.description) == unicode)
    finally:
        os.remove(data_file.name)
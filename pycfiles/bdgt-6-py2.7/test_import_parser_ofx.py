# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_import_parser_ofx.py
# Compiled at: 2014-10-09 13:38:05
import datetime, os, tempfile
from decimal import Decimal
from nose.tools import eq_, ok_
from bdgt.importer.parsers import OfxParser

def test_parse():
    ofx_file = tempfile.NamedTemporaryFile(delete=False)
    try:
        with ofx_file as (f):
            f.write('\n            <OFX>\n                <SIGNONMSGSRSV1>\n                <SONRS>\n                    <STATUS>\n                    <CODE>0\n                    <SEVERITY>INFO\n                    </STATUS>\n                    <DTSERVER>20071015021529.000[-8:PST]\n                    <LANGUAGE>ENG\n                    <DTACCTUP>19900101000000\n                    <FI>\n                    <ORG>MYBANK\n                    <FID>01234\n                    </FI>\n                </SONRS>\n                </SIGNONMSGSRSV1>\n                <BANKMSGSRSV1>\n                    <STMTTRNRS>\n                    <TRNUID>23382938\n                    <STATUS>\n                        <CODE>0\n                        <SEVERITY>INFO\n                    </STATUS>\n                    <STMTRS>\n                        <CURDEF>USD\n                        <BANKACCTFROM>\n                        <BANKID>987654321\n                        <ACCTID>098-121\n                        <ACCTTYPE>SAVINGS\n                        </BANKACCTFROM>\n                        <BANKTRANLIST>\n                        <DTSTART>20070101\n                        <DTEND>20071015\n                        <STMTTRN>\n                            <TRNTYPE>CREDIT\n                            <DTPOSTED>20070315\n                            <DTUSER>20070315\n                            <TRNAMT>200.00\n                            <FITID>980315001\n                            <NAME>DEPOSIT\n                            <MEMO>description lines\n                        </STMTTRN>\n                        </BANKTRANLIST>\n                        <LEDGERBAL>\n                        <BALAMT>5250.00\n                        <DTASOF>20071015021529.000[-8:PST]\n                        </LEDGERBAL>\n                        <AVAILBAL>\n                        <BALAMT>5250.00\n                        <DTASOF>20071015021529.000[-8:PST]\n                        </AVAILBAL>\n                    </STMTRS>\n                    </STMTTRNRS>\n                </BANKMSGSRSV1>\n            </OFX>\n            ')
        parser = OfxParser()
        txs = parser.parse(ofx_file.name)
        eq_(len(txs), 1)
        eq_(txs[0].parsed_tx.date, datetime.date(2007, 3, 15))
        eq_(txs[0].parsed_tx.account, '098-121')
        ok_('description lines' in txs[0].parsed_tx.description)
        eq_(txs[0].parsed_tx.amount, Decimal('200.00'))
    finally:
        os.remove(ofx_file.name)
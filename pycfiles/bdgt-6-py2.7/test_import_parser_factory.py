# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tests/test_import_parser_factory.py
# Compiled at: 2014-10-09 13:38:05
from nose.tools import ok_, raises
from bdgt.importer.parsers import Mt940Parser
from bdgt.importer.parsers import TxParserFactory

def test_tx_parser_factory():
    parser = TxParserFactory.create('mt940')
    ok_(isinstance(parser, Mt940Parser))


@raises(ValueError)
def test_tx_parser_factory_unknown_type():
    TxParserFactory.create('unknown')
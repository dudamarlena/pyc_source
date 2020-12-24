# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_consultas\test_abandonadas_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest
from decimal import Decimal
from ...core.base_classes import TagDataHoraUTC

class ClasseTransacaoAbandonadasTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<transactionSearchResult>\n    <date>2011-02-16T20:14:35.000-02:00</date>\n    <currentPage>1</currentPage>\n    <resultsInThisPage>2</resultsInThisPage>\n    <totalPages>1</totalPages>\n    <transactions>\n        <transaction>\n            <date>2011-02-05T15:46:12.000-02:00</date>\n            <lastEventDate>2011-02-15T17:39:14.000-03:00</lastEventDate>\n            <code>EDDDC505-8A26-494E-96C2-53D285A470C2</code>\n            <type>1</type>\n            <grossAmount>6.00</grossAmount>\n        </transaction>\n        <transaction>\n            <date>2011-02-07T18:57:52.000-02:00</date>\n            <lastEventDate>2011-02-14T21:37:24.000-03:00</lastEventDate>\n            <reference>REFCODE2</reference>\n            <code>97B1F57E-0EC0-4D03-BF7E-C4694CF6062E</code>\n            <type>1</type>\n            <grossAmount>6.00</grossAmount>\n        </transaction>\n    </transactions>\n</transactionSearchResult> '

    def test_parse_xml(self):
        from pagseguro_xml.consultas.v2.classes import ClasseTransacaoAbandonadas
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseTransacaoAbandonadas"')
        result = ClasseTransacaoAbandonadas()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        data = TagDataHoraUTC()
        data.valor = '2011-02-16T20:14:35.000-02:00'
        log.debug('Testando valores da "transactionSearchResult"')
        self.assertEqual(result.date.valor, data.valor)
        self.assertEqual(result.currentPage.valor, 1)
        self.assertEqual(result.resultsInThisPage.valor, 2)
        self.assertEqual(result.totalPages.valor, 1)
        self.assertEqual(len(result.transactions), 2)
        log.debug('Valores da "transactionSearchResult" OK')
        transactionsFilhos = [
         {'date': '2011-02-05T15:46:12.000-02:00', 
            'lastEventDate': '2011-02-15T17:39:14.000-03:00', 
            'code': 'EDDDC505-8A26-494E-96C2-53D285A470C2', 
            'reference': '', 
            'type': 1, 
            'grossAmount': Decimal('6.00')},
         {'date': '2011-02-07T18:57:52.000-02:00', 
            'lastEventDate': '2011-02-14T21:37:24.000-03:00', 
            'code': '97B1F57E-0EC0-4D03-BF7E-C4694CF6062E', 
            'reference': 'REFCODE2', 
            'type': 1, 
            'grossAmount': Decimal('6.00')}]
        log.debug('Testando valores das "transactions"')
        for i, transaction in enumerate(result.transactions):
            log.debug('Transactions No: %s' % (i + 1))
            data.valor = transactionsFilhos[i]['date']
            self.assertEqual(transaction.date.valor, data.valor)
            data.valor = transactionsFilhos[i]['lastEventDate']
            self.assertEqual(transaction.lastEventDate.valor, data.valor)
            self.assertEqual(transaction.reference.valor, transactionsFilhos[i]['reference'])
            self.assertEqual(transaction.type.valor, transactionsFilhos[i]['type'])
            self.assertEqual(transaction.grossAmount.valor, transactionsFilhos[i]['grossAmount'])
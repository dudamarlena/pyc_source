# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_consultas\test_historico_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest
from decimal import Decimal
from ...core.base_classes import TagDataHoraUTC

class ClasseTransacaoHistoricoTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<transactionSearchResult>\n    <date>2011-02-16T20:14:35.000-02:00</date>\n    <currentPage>1</currentPage>\n    <resultsInThisPage>10</resultsInThisPage>\n    <totalPages>1</totalPages>\n    <transactions>\n        <transaction>\n            <date>2011-02-05T15:46:12.000-02:00</date>\n            <lastEventDate>2011-02-15T17:39:14.000-03:00</lastEventDate>\n            <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>\n            <reference>REF1234</reference>\n            <type>1</type>\n            <status>3</status>\n            <paymentMethod>\n                <type>1</type>\n            </paymentMethod>\n            <grossAmount>49900.00</grossAmount>\n            <discountAmount>0.00</discountAmount>\n            <feeAmount>0.00</feeAmount>\n            <netAmount>49900.00</netAmount>\n            <extraAmount>0.00</extraAmount>\n        </transaction>\n        <transaction>\n            <date>2011-02-07T18:57:52.000-02:00</date>\n            <lastEventDate>2011-02-14T21:37:24.000-03:00</lastEventDate>\n            <code>2FB07A22-68FF-4F83-A356-24153A0C05E1</code>\n            <reference>REF5678</reference>\n            <type>3</type>\n            <status>4</status>\n            <paymentMethod>\n                <type>3</type>\n            </paymentMethod>\n            <grossAmount>26900.00</grossAmount>\n            <discountAmount>0.00</discountAmount>\n            <feeAmount>0.00</feeAmount>\n            <netAmount>26900.00</netAmount>\n            <extraAmount>0.00</extraAmount>\n        </transaction>\n    </transactions>\n</transactionSearchResult>'

    def test_parse_xml(self):
        from pagseguro_xml.consultas.v2.classes import ClasseTransacaoHistorico
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseTransacaoHistorico"')
        result = ClasseTransacaoHistorico()
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
        self.assertEqual(result.resultsInThisPage.valor, 10)
        self.assertEqual(result.totalPages.valor, 1)
        self.assertEqual(len(result.transactions), 2)
        log.debug('Valores da "transactionSearchResult" OK')
        transactionsFilhos = [
         {'date': '2011-02-05T15:46:12.000-02:00', 
            'lastEventDate': '2011-02-15T17:39:14.000-03:00', 
            'code': '9E884542-81B3-4419-9A75-BCC6FB495EF1', 
            'reference': 'REF1234', 
            'type': 1, 
            'status': 3, 
            'paymentMethod.type': 1, 
            'grossAmount': Decimal('49900.00'), 
            'discountAmount': Decimal('0.00'), 
            'feeAmount': Decimal('0.00'), 
            'netAmount': Decimal('49900.00'), 
            'extraAmount': Decimal('0.00')},
         {'date': '2011-02-07T18:57:52.000-02:00', 
            'lastEventDate': '2011-02-14T21:37:24.000-03:00', 
            'code': '2FB07A22-68FF-4F83-A356-24153A0C05E1', 
            'reference': 'REF5678', 
            'type': 3, 
            'status': 4, 
            'paymentMethod.type': 3, 
            'grossAmount': Decimal('26900.00'), 
            'discountAmount': Decimal('0.00'), 
            'feeAmount': Decimal('0.00'), 
            'netAmount': Decimal('26900.00'), 
            'extraAmount': Decimal('0.00')}]
        log.debug('Testando valores das "transactions"')
        for i, transaction in enumerate(result.transactions):
            log.debug('Transactions No: %s' % (i + 1))
            data.valor = transactionsFilhos[i]['date']
            self.assertEqual(transaction.date.valor, data.valor)
            data.valor = transactionsFilhos[i]['lastEventDate']
            self.assertEqual(transaction.lastEventDate.valor, data.valor)
            self.assertEqual(transaction.reference.valor, transactionsFilhos[i]['reference'])
            self.assertEqual(transaction.type.valor, transactionsFilhos[i]['type'])
            self.assertEqual(transaction.status.valor, transactionsFilhos[i]['status'])
            self.assertEqual(transaction.paymentMethod.type.valor, transactionsFilhos[i]['paymentMethod.type'])
            self.assertEqual(transaction.grossAmount.valor, transactionsFilhos[i]['grossAmount'])
            self.assertEqual(transaction.discountAmount.valor, transactionsFilhos[i]['discountAmount'])
            self.assertEqual(transaction.feeAmount.valor, transactionsFilhos[i]['feeAmount'])
            self.assertEqual(transaction.netAmount.valor, transactionsFilhos[i]['netAmount'])
            self.assertEqual(transaction.extraAmount.valor, transactionsFilhos[i]['extraAmount'])
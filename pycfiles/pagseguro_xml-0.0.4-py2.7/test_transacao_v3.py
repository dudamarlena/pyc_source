# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_notificacao\test_transacao_v3.py
# Compiled at: 2015-12-29 16:38:09
import unittest, logging, sys
from ...core.base_classes import TagDataHoraUTC
from decimal import Decimal

class ClasseNotificacaoTransacaoTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<transaction>\n        <date>2011-02-10T16:13:41.000-03:00</date>\n        <code>9E884542-81B3-4419-9A75-BCC6FB495EF1</code>\n        <reference>REF1234</reference>\n        <type>1</type>\n        <status>3</status>\n        <paymentMethod>\n            <type>1</type>\n            <code>101</code>\n        </paymentMethod>\n        <grossAmount>49900.00</grossAmount>\n        <discountAmount>0.00</discountAmount>\n        <creditorFees>\n            <intermediationRateAmount>0.40</intermediationRateAmount>\n            <intermediationFeeAmount>1644.80</intermediationFeeAmount>\n        </creditorFees>\n        <netAmount>49900.00</netAmount>\n        <extraAmount>0.00</extraAmount>\n        <installmentCount>1</installmentCount>\n        <itemCount>2</itemCount>\n        <items>\n            <item>\n                <id>0001</id>\n                <description>Notebook Prata</description>\n                <quantity>1</quantity>\n                <amount>24300.00</amount>\n            </item>\n            <item>\n                <id>0002</id>\n                <description>Notebook Rosa</description>\n                <quantity>1</quantity>\n                <amount>25600.00</amount>\n            </item>\n        </items>\n        <sender>\n            <name>José Comprador</name>\n            <email>comprador@uol.com.br</email>\n            <phone>\n                <areaCode>11</areaCode>\n                <number>56273440</number>\n            </phone>\n        </sender>\n        <shipping>\n            <address>\n                <street>Av. Brig. Faria Lima</street>\n                <number>1384</number>\n                <complement>5o andar</complement>\n                <district>Jardim Paulistano</district>\n                <postalCode>01452002</postalCode>\n                <city>Sao Paulo</city>\n                <state>SP</state>\n                <country>BRA</country>\n            </address>\n            <type>1</type>\n            <cost>21.50</cost>\n        </shipping>\n</transaction>'

    def test_parse_xml(self):
        from ...notificacao.v3.classes import ClasseNotificacaoTransacao
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseNotificacaoTransacao_v3"')
        result = ClasseNotificacaoTransacao()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        log.debug('Testando valores da "transaction"')
        data = TagDataHoraUTC()
        data.valor = '2011-02-10T16:13:41.000-03:00'
        self.assertEqual(result.date.valor, data.valor)
        self.assertEqual(result.code.valor, '9E884542-81B3-4419-9A75-BCC6FB495EF1')
        self.assertEqual(result.reference.valor, 'REF1234')
        self.assertEqual(result.type.valor, 1)
        self.assertEqual(result.status.valor, 3)
        self.assertEqual(result.paymentMethod.type.valor, 1)
        self.assertEqual(result.paymentMethod.code.valor, 101)
        self.assertEqual(result.grossAmount.valor, Decimal('49900.00'))
        self.assertEqual(result.discountAmount.valor, Decimal('0.00'))
        self.assertEqual(result.creditorFees.intermediationRateAmount.valor, Decimal('0.40'))
        self.assertEqual(result.creditorFees.intermediationFeeAmount.valor, Decimal('1644.80'))
        self.assertEqual(result.netAmount.valor, Decimal('49900.00'))
        self.assertEqual(result.extraAmount.valor, Decimal('0.00'))
        self.assertEqual(result.installmentCount.valor, 1)
        self.assertEqual(result.itemCount.valor, 2)
        self.assertEqual(len(result.items), 2)
        log.debug('Valores da "transacao" OK')
        items = [
         {'id': '0001', 
            'description': 'Notebook Prata', 
            'quantity': Decimal('1.00'), 
            'amount': Decimal('24300.00')},
         {'id': '0002', 
            'description': 'Notebook Rosa', 
            'quantity': Decimal('1.00'), 
            'amount': Decimal('25600.00')}]
        log.debug('Testando valores dos "itens"')
        for i, item in enumerate(result.items):
            log.debug('Item No: %s' % (i + 1))
            self.assertEqual(item.ID.valor, items[i]['id'])
            self.assertEqual(item.description.valor, items[i]['description'])
            self.assertEqual(item.quantity.valor, items[i]['quantity'])
            self.assertEqual(item.amount.valor, items[i]['amount'])

        log.debug('Testando dados do "comprador"')
        self.assertEqual(result.sender.name.valor, 'José Comprador')
        self.assertEqual(result.sender.email.valor, 'comprador@uol.com.br')
        self.assertEqual(result.sender.phone.areaCode.valor, 11)
        self.assertEqual(result.sender.phone.number.valor, 56273440)
        log.debug('Testando dados do "endereco" do comprador')
        self.assertEqual(result.shipping.address.street.valor, 'Av. Brig. Faria Lima')
        self.assertEqual(result.shipping.address.number.valor, '1384')
        self.assertEqual(result.shipping.address.complement.valor, '5o andar')
        self.assertEqual(result.shipping.address.district.valor, 'Jardim Paulistano')
        self.assertEqual(result.shipping.address.city.valor, 'Sao Paulo')
        self.assertEqual(result.shipping.address.state.valor, 'SP')
        self.assertEqual(result.shipping.address.country.valor, 'BRA')
        self.assertEqual(result.shipping.address.postalCode.valor, '01452002')
        self.assertEqual(result.shipping.type.valor, 1)
        self.assertEqual(result.shipping.cost.valor, Decimal('21.50'))
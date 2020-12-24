# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_consultas\test_detalhes_v3.py
# Compiled at: 2015-12-29 16:38:09
import unittest, logging, sys
from ...core.base_classes import TagDataHoraUTC
from decimal import Decimal

class ClasseTransacaoDetalhesTest(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<transaction>\n    <date>2015-12-10T14:32:54.000-02:00</date>\n    <code>B8CFB1D5-7E2E-4775-B747-6CD9B927738D</code>\n    <reference>REF0001</reference>\n    <type>11</type>\n    <status>1</status>\n    <lastEventDate>2015-12-10T14:32:54.000-02:00</lastEventDate>\n    <paymentMethod>\n        <type>1</type>\n        <code>101</code>\n    </paymentMethod>\n    <grossAmount>1.00</grossAmount>\n    <discountAmount>0.00</discountAmount>\n    <creditorFees>\n        <installmentFeeAmount>0.00</installmentFeeAmount>\n        <intermediationRateAmount>0.40</intermediationRateAmount>\n        <intermediationFeeAmount>0.04</intermediationFeeAmount>\n    </creditorFees>\n    <netAmount>0.56</netAmount>\n    <installmentCount>1</installmentCount>\n    <itemCount>1</itemCount>\n    <items>\n        <item>\n            <id>001</id>\n            <description>Plano simples de 6 meses por R$ 1,00</description>\n            <quantity>1</quantity>\n            <amount>1.00</amount>\n        </item>\n    </items>\n    <sender>\n        <name>ALGUEM DA CUNHA</name>\n        <email>teste1234@sandbox.pagseguro.com.br</email>\n        <phone>\n            <areaCode>63</areaCode>\n            <number>92111111</number>\n        </phone>\n    </sender>\n    <shipping>\n        <address>\n            <street>RUA</street>\n            <number>1</number>\n            <complement></complement>\n            <district>Centro</district>\n            <city>PALMAS</city>\n            <state>TO</state>\n            <country>BRA</country>\n            <postalCode>77000000</postalCode>\n        </address>\n        <type>3</type>\n        <cost>0.00</cost>\n    </shipping>\n</transaction>'

    def test_parse_xml(self):
        from ...consultas.v3.classes import ClasseTransacaoDetalhes
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseTransacaoDetalhes"')
        result = ClasseTransacaoDetalhes()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        log.debug('Testando valores da "transaction"')
        data = TagDataHoraUTC()
        data.valor = '2015-12-10T14:32:54.000-02:00'
        self.assertEqual(result.date.valor, data.valor)
        self.assertEqual(result.code.valor, 'B8CFB1D5-7E2E-4775-B747-6CD9B927738D')
        self.assertEqual(result.reference.valor, 'REF0001')
        self.assertEqual(result.type.valor, 11)
        self.assertEqual(result.status.valor, 1)
        data.valor = '2015-12-10T14:32:54.000-02:00'
        self.assertEqual(result.lastEventDate.valor, data.valor)
        self.assertEqual(result.paymentMethod.type.valor, 1)
        self.assertEqual(result.paymentMethod.code.valor, 101)
        self.assertEqual(result.grossAmount.valor, Decimal('1.00'))
        self.assertEqual(result.discountAmount.valor, Decimal('0.00'))
        self.assertEqual(result.creditorFees.installmentFeeAmount.valor, Decimal('0.00'))
        self.assertEqual(result.creditorFees.intermediationRateAmount.valor, Decimal('0.40'))
        self.assertEqual(result.creditorFees.intermediationFeeAmount.valor, Decimal('0.04'))
        self.assertEqual(result.netAmount.valor, Decimal('0.56'))
        self.assertEqual(result.installmentCount.valor, 1)
        self.assertEqual(result.itemCount.valor, 1)
        self.assertEqual(len(result.items), 1)
        log.debug('Valores da "transacao" OK')
        items = [
         {'id': '001', 
            'description': 'Plano simples de 6 meses por R$ 1,00', 
            'quantity': Decimal('1.00'), 
            'amount': Decimal('1.00')}]
        log.debug('Testando valores dos "itens"')
        for i, item in enumerate(result.items):
            log.debug('Item No: %s' % (i + 1))
            self.assertEqual(item.ID.valor, items[i]['id'])
            self.assertEqual(item.description.valor, items[i]['description'])
            self.assertEqual(item.quantity.valor, items[i]['quantity'])
            self.assertEqual(item.amount.valor, items[i]['amount'])

        log.debug('Testando dados do "comprador"')
        self.assertEqual(result.sender.name.valor, 'ALGUEM DA CUNHA')
        self.assertEqual(result.sender.email.valor, 'teste1234@sandbox.pagseguro.com.br')
        self.assertEqual(result.sender.phone.areaCode.valor, 63)
        self.assertEqual(result.sender.phone.number.valor, 92111111)
        log.debug('Testando dados do "endereco" do comprador')
        self.assertEqual(result.shipping.address.street.valor, 'RUA')
        self.assertEqual(result.shipping.address.number.valor, '1')
        self.assertEqual(result.shipping.address.complement.valor, '')
        self.assertEqual(result.shipping.address.district.valor, 'Centro')
        self.assertEqual(result.shipping.address.city.valor, 'PALMAS')
        self.assertEqual(result.shipping.address.state.valor, 'TO')
        self.assertEqual(result.shipping.address.country.valor, 'BRA')
        self.assertEqual(result.shipping.address.postalCode.valor, '77000000')
        self.assertEqual(result.shipping.type.valor, 3)
        self.assertEqual(result.shipping.cost.valor, Decimal('0.00'))
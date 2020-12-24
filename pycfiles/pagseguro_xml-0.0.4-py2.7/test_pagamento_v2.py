# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_pagamento\test_pagamento_v2.py
# Compiled at: 2015-12-29 16:38:09
import unittest, logging, sys
from decimal import Decimal

class ClassePagamentoCheckoutV2Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<checkout>\n    <reference>REF1234</reference>\n    <currency>BRL</currency>\n    <items>\n        <item>\n            <id>0001</id>\n            <description>Notebook Prata</description>\n            <amount>24300.00</amount>\n            <quantity>1</quantity>\n            <weight>1000</weight>\n        </item>\n        <item>\n            <id>0002</id>\n            <description>Notebook Rosa</description>\n            <amount>25600.00</amount>\n            <quantity>2</quantity>\n            <weight>750</weight>\n        </item>\n    </items>\n    <sender>\n        <name>José Comprador</name>\n        <email>comprador@uol.com.br</email>\n        <phone>\n            <areaCode>11</areaCode>\n            <number>56273440</number>\n        </phone>\n    </sender>\n    <shipping>\n        <type>1</type>\n        <address>\n            <street>Av. Brig. Faria Lima</street>\n            <number>1384</number>\n            <complement>5o andar</complement>\n            <district>Jardim Paulistano</district>\n            <postalCode>01452002</postalCode>\n            <city>Sao Paulo</city>\n            <state>SP</state>\n            <country>BRA</country>\n        </address>\n    </shipping>\n</checkout>'

    def test_parse_xml(self):
        from ...pagamento.v2.classes import ClassePagamentoCheckout
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClassePagamentoCheckout_v2"')
        result = ClassePagamentoCheckout()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        log.debug('Testando valores da "checkout"')
        self.assertEqual(result.reference.valor, 'REF1234')
        self.assertEqual(result.currency.valor, 'BRL')
        self.assertEqual(len(result.items), 2)
        log.debug('Valores da "checkout" OK')
        items = [
         {'id': '0001', 
            'description': 'Notebook Prata', 
            'amount': Decimal('24300.00'), 
            'quantity': 1, 
            'weight': 1000},
         {'id': '0002', 
            'description': 'Notebook Rosa', 
            'amount': Decimal('25600.00'), 
            'quantity': 2, 
            'weight': 750}]
        log.debug('Testando valores dos "itens"')
        for i, item in enumerate(result.items):
            log.debug('Item No: %s' % (i + 1))
            self.assertEqual(item.ID.valor, items[i]['id'])
            self.assertEqual(item.description.valor, items[i]['description'])
            self.assertEqual(item.amount.valor, items[i]['amount'])
            self.assertEqual(item.quantity.valor, items[i]['quantity'])
            self.assertEqual(item.weight.valor, items[i]['weight'])

        log.debug('Testando dados do "comprador"')
        self.assertEqual(result.sender.name.valor, 'José Comprador')
        self.assertEqual(result.sender.email.valor, 'comprador@uol.com.br')
        self.assertEqual(result.sender.phone.areaCode.valor, 11)
        self.assertEqual(result.sender.phone.number.valor, 56273440)
        log.debug('Testando dados do "endereco" do comprador')
        self.assertEqual(result.shipping.type.valor, 1)
        self.assertEqual(result.shipping.address.street.valor, 'Av. Brig. Faria Lima')
        self.assertEqual(result.shipping.address.number.valor, '1384')
        self.assertEqual(result.shipping.address.complement.valor, '5o andar')
        self.assertEqual(result.shipping.address.district.valor, 'Jardim Paulistano')
        self.assertEqual(result.shipping.address.city.valor, 'Sao Paulo')
        self.assertEqual(result.shipping.address.state.valor, 'SP')
        self.assertEqual(result.shipping.address.country.valor, 'BRA')


class ClassePagamentoRetornoCheckoutV2Test(unittest.TestCase):

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<checkout>\n    <code>8CF4BE7DCECEF0F004A6DFA0A8243412</code>\n    <date>2010-12-02T10:11:28.000-02:00</date>\n</checkout>  '

    def test_parse_xml(self):
        from ...pagamento.v2.classes import ClassePagamentoRetornoCheckout
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClassePagamentoRetornoCheckout_v2"')
        result = ClassePagamentoRetornoCheckout()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        log.debug('Testando valores da "checkout"')
        from ...core.base_classes import TagDataHoraUTC
        date = TagDataHoraUTC()
        date.valor = '2010-12-02T10:11:28.000-02:00'
        self.assertEqual(result.code.valor, '8CF4BE7DCECEF0F004A6DFA0A8243412')
        self.assertEqual(result.date.valor, date.valor)
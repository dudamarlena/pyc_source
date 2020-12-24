# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_assinatura\test_requisicao_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest
from decimal import Decimal
from ...core.base_classes import TagDataHoraUTC

class ClasseAssinaturaRequisicaoTest(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.assinatura.v2.classes import ClasseAssinaturaRequisicao
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseAssinaturaRequisicao"')
        result = ClasseAssinaturaRequisicao()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        data = TagDataHoraUTC()
        log.debug('Testando valores da "preApprovalRequest"')
        self.assertEqual(result.redirectURL.valor, 'http://www.seusite.com.br/retorno.php')
        self.assertEqual(result.reviewURL.valor, 'http://www.seusite.com.br/revisao.php')
        self.assertEqual(result.reference.valor, 'REF1234')
        self.assertEqual(result.receiver.email.valor, 'nao@sei.com')
        self.assertEqual(result.sender.email.valor, 'cliente@uol.com.br')
        self.assertEqual(result.sender.name.valor, 'Nome do Cliente')
        self.assertEqual(result.sender.phone.areaCode.valor, 11)
        self.assertEqual(result.sender.phone.number.valor, 56273440)
        self.assertEqual(result.sender.address.street.valor, 'Avenida Brigadeiro Faria Lima')
        self.assertEqual(result.sender.address.number.valor, '1384')
        self.assertEqual(result.sender.address.complement.valor, 'Andar')
        self.assertEqual(result.sender.address.district.valor, 'Jardim Paulistano')
        self.assertEqual(result.sender.address.postalCode.valor, '01452002')
        self.assertEqual(result.sender.address.city.valor, 'São Paulo')
        self.assertEqual(result.sender.address.state.valor, 'SP')
        self.assertEqual(result.sender.address.country.valor, 'BRA')
        self.assertEqual(result.preApproval.charge.valor, 'auto')
        self.assertEqual(result.preApproval.name.valor, 'Seguro contra roubo do Notebook')
        self.assertEqual(result.preApproval.details.valor, 'Todo dia 28 será cobrado o valor de R$100,00 referente ao seguro contra roubo de Notebook')
        self.assertEqual(result.preApproval.amountPerPayment.valor, Decimal('100.00'))
        self.assertEqual(result.preApproval.period.valor, 'MONTHLY')
        data.valor = '2014-01-21T00:00:000-03:00'
        self.assertEqual(result.preApproval.finalDate.valor, data.valor)
        self.assertEqual(result.preApproval.maxTotalAmount.valor, Decimal('2400.00'))
        log.debug('Valores da "preApprovalRequest" OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<preApprovalRequest>\n    <redirectURL>http://www.seusite.com.br/retorno.php</redirectURL>\n    <reviewURL>http://www.seusite.com.br/revisao.php</reviewURL>\n    <reference>REF1234</reference>\n    <receiver>\n        <email>nao@sei.com</email>\n    </receiver>\n    <sender>\n        <name>Nome do Cliente</name>\n        <email>cliente@uol.com.br</email>\n        <phone>\n            <areaCode>11</areaCode>\n            <number>56273440</number>\n        </phone>\n        <address>\n            <street>Avenida Brigadeiro Faria Lima</street>\n            <number>1384</number>\n            <complement>Andar</complement>\n            <district>Jardim Paulistano</district>\n            <postalCode>01452002</postalCode>\n            <city>São Paulo</city>\n            <state>SP</state>\n            <country>BRA</country>\n        </address>\n    </sender>\n    <preApproval>\n        <charge>auto</charge>\n        <name>Seguro contra roubo do Notebook</name>\n        <details>Todo dia 28 será cobrado o valor de R$100,00 referente ao seguro contra roubo de Notebook</details>\n        <amountPerPayment>100.00</amountPerPayment>\n        <period>MONTHLY</period>\n        <finalDate>2014-01-21T00:00:000-03:00</finalDate>\n        <maxTotalAmount>2400.00</maxTotalAmount>\n    </preApproval>\n</preApprovalRequest>'


class ClasseAssinaturaRespostaTest(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.assinatura.v2.classes import ClasseAssinaturaResposta
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseAssinaturaResposta"')
        result = ClasseAssinaturaResposta()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        data = TagDataHoraUTC()
        data.valor = '2014-01-21T00:00:00.000-03:00'
        log.debug('Testando valores da "preApprovalRequest"')
        self.assertEqual(result.code.valor, 'DC2DAC98FBFBDD1554493F94E85FAE05')
        self.assertEqual(result.date.valor, data.valor)
        log.debug('Valores da "preApprovalRequest" OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<preApprovalRequest>\n    <code>DC2DAC98FBFBDD1554493F94E85FAE05</code>\n    <date>2014-01-21T00:00:00.000-03:00</date>\n</preApprovalRequest>'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_assinatura\test_consulta_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest
from ...core.base_classes import TagDataHoraUTC

class ClasseConsultaAssinaturaRespostaTest(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.assinatura.v2.classes import ClasseConsultaAssinaturaResposta
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseConsultaAssinaturaResposta"')
        result = ClasseConsultaAssinaturaResposta()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        data = TagDataHoraUTC()
        log.debug('Verificando os dados de "preApproval"')
        self.assertEqual(result.name.valor, 'Seguro contra roubo do Notebook Prata')
        self.assertEqual(result.code.valor, 'C08984179E9EDF3DD4023F87B71DE349')
        data.valor = '2011-11-23T13:40:23.000-02:00'
        self.assertEqual(result.date.valor, data.valor)
        self.assertEqual(result.tracker.valor, '538C53')
        self.assertEqual(result.status.valor, 'CANCELLED')
        self.assertEqual(result.reference.valor, 'REF1234')
        data.valor = '2011-11-25T20:04:23.000-02:00'
        self.assertEqual(result.lastEventDate.valor, data.valor)
        self.assertEqual(result.charge.valor, 'auto')
        log.debug('Verificando os dados de "sender" (comprador)')
        self.assertEqual(result.sender.name.valor, 'Nome Comprador')
        self.assertEqual(result.sender.email.valor, 'comprador@uol.com')
        self.assertEqual(result.sender.phone.areaCode.valor, 11)
        self.assertEqual(result.sender.phone.number.valor, 30389678)
        self.assertEqual(result.sender.address.street.valor, 'ALAMEDA ITU')
        self.assertEqual(result.sender.address.number.valor, '78')
        self.assertEqual(result.sender.address.complement.valor, 'ap. 2601')
        self.assertEqual(result.sender.address.district.valor, 'Jardim Paulista')
        self.assertEqual(result.sender.address.city.valor, 'SAO PAULO')
        self.assertEqual(result.sender.address.country.valor, 'BRA')
        self.assertEqual(result.sender.address.postalCode.valor, '01421000')
        log.debug('Dados OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<preApproval>\n    <name>Seguro contra roubo do Notebook Prata</name>\n    <code>C08984179E9EDF3DD4023F87B71DE349</code>\n    <date>2011-11-23T13:40:23.000-02:00</date>\n    <tracker>538C53</tracker>\n    <status>CANCELLED</status>\n    <reference>REF1234</reference>\n    <lastEventDate>2011-11-25T20:04:23.000-02:00</lastEventDate>\n    <charge>auto</charge>\n    <sender>\n        <name>Nome Comprador</name>\n        <email>comprador@uol.com</email>\n        <phone>\n            <areaCode>11</areaCode>\n            <number>30389678</number>\n        </phone>\n        <address>\n            <street>ALAMEDA ITU</street>\n            <number>78</number>\n            <complement>ap. 2601</complement>\n            <district>Jardim Paulista</district>\n            <city>SAO PAULO</city>\n            <state>SP</state>\n            <country>BRA</country>\n            <postalCode>01421000</postalCode>\n        </address>\n    </sender>\n</preApproval>'


class ClasseConsultaAssinaturasRespostaTest(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.assinatura.v2.classes import ClasseConsultaAssinaturasResposta
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseConsultaAssinaturasResposta"')
        result = ClasseConsultaAssinaturasResposta()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        data = TagDataHoraUTC()
        log.debug('Verificando os dados de "preApprovalSearchResult"')
        self.assertEqual(result.resultsInThisPage.valor, 1)
        self.assertEqual(result.currentPage.valor, 1)
        self.assertEqual(result.totalPages.valor, 1)
        data.valor = '2011-08-08T16:16:23.000-03:00'
        self.assertEqual(result.date.valor, data.valor)
        itens = [
         {'name': 'PagSeguro Pre Approval', 
            'code': '12E10BEF5E5EF94004313FB891C8E4CF', 
            'date': '2011-08-15T11:06:44.000-03:00', 
            'tracker': '624C17', 
            'status': 'INITIATED', 
            'reference': 'R123456', 
            'lastEventDate': '2011-08-08T15:37:30.000-03:00', 
            'charge': 'auto'}]
        log.debug('Verificando a list de "preAproval"')
        for i, preApproval in enumerate(result.preApprovals):
            log.debug('Testando valores do preApproval No "%s"' % (i + 1))
            self.assertEqual(preApproval.name.valor, itens[i]['name'])
            self.assertEqual(preApproval.code.valor, itens[i]['code'])
            data.valor = itens[i]['date']
            self.assertEqual(preApproval.date.valor, data.valor)
            self.assertEqual(preApproval.tracker.valor, itens[i]['tracker'])
            self.assertEqual(preApproval.status.valor, itens[i]['status'])
            self.assertEqual(preApproval.reference.valor, itens[i]['reference'])
            data.valor = itens[i]['lastEventDate']
            self.assertEqual(preApproval.lastEventDate.valor, data.valor)
            self.assertEqual(preApproval.charge.valor, itens[i]['charge'])

        log.debug('Dados OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<preApprovalSearchResult>\n    <resultsInThisPage>1</resultsInThisPage>\n    <currentPage>1</currentPage>\n    <totalPages>1</totalPages>\n    <date>2011-08-08T16:16:23.000-03:00</date>\n    <preApprovals>\n        <preApproval>\n            <name>PagSeguro Pre Approval</name>\n            <code>12E10BEF5E5EF94004313FB891C8E4CF</code>\n            <date>2011-08-15T11:06:44.000-03:00</date>\n            <tracker>624C17</tracker>\n            <status>INITIATED</status>\n            <reference>R123456</reference>\n            <lastEventDate>2011-08-08T15:37:30.000-03:00</lastEventDate>\n            <charge>auto</charge>\n        </preApproval>\n    </preApprovals>\n</preApprovalSearchResult>\n'
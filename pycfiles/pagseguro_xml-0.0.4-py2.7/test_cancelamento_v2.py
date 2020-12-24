# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_assinatura\test_cancelamento_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest
from ...core.base_classes import TagDataHoraUTC

class ClasseCancelamentoAssinaturaRetornoTest(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.assinatura.v2.classes import ClasseCancelamentoAssinaturaRetorno
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClasseCancelamentoAssinaturaRetorno"')
        result = ClasseCancelamentoAssinaturaRetorno()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        log.debug('Verificando a list de erros')
        data = TagDataHoraUTC()
        data.valor = '2011-08-31T13:43:23.000-03:00'
        log.debug('Testando valores da "result"')
        self.assertEqual(result.date.valor, data.valor)
        self.assertEqual(result.status.valor, 'OK')
        log.debug('Errors OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<result>\n    <date>2011-08-31T13:43:23.000-03:00</date>\n    <status>OK</status>\n</result>'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\tests\test_classes_pagamento\test_erros_v2.py
# Compiled at: 2015-12-29 16:38:09
import logging, sys, unittest

class ClassePagamentoErrosV2Test(unittest.TestCase):

    def test_parse_xml(self):
        from pagseguro_xml.pagamento.v2.classes import ClassePagamentoErros
        log = self.logger.getLogger('%s.%s' % (__package__, self.__class__.__name__))
        log.debug('Criando instancia de "ClassePagamentoErros_v2"')
        result = ClassePagamentoErros()
        log.debug('Gerando PARSE do xml')
        result.xml = self.xml
        log.debug('Quantidade de alertas no "parse": %s' % len(result.alertas))
        for a in result.alertas:
            log.debug('Alerta: %s' % a)

        itens = [
         {'code': '11004', 
            'message': 'Currency is required.'},
         {'code': '11005', 
            'message': 'Currency invalid value: 100'}]
        log.debug('Verificando a list de erros')
        for i, error in enumerate(result.errors):
            log.debug('Testando valores do error No "%s"' % (i + 1))
            self.assertEqual(error.code.valor, itens[i]['code'])
            self.assertEqual(error.message.valor, itens[i]['message'])

        log.debug('Errors OK')

    def setUp(self):
        logging.basicConfig(stream=sys.stderr)
        logging.getLogger('%s.%s' % (__package__, self.__class__.__name__)).setLevel(logging.DEBUG)
        self.logger = logging
        self.xml = '<?xml version="1.0" encoding="ISO-8859-1" standalone="yes"?>\n<errors>\n    <error>\n        <code>11004</code>\n        <message>Currency is required.</message>\n    </error>\n    <error>\n        <code>11005</code>\n        <message>Currency invalid value: 100</message>\n    </error>\n</errors> '
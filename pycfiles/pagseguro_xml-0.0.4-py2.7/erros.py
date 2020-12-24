# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\pagamento\v2\classes\erros.py
# Compiled at: 2015-12-29 16:38:09
from __future__ import division, print_function, unicode_literals
from ....core.base_classes import ABERTURA, TagCaracter, XMLAPI
from ....core import CONST

class Error(XMLAPI):

    def __init__(self):
        super(Error, self).__init__()
        self.code = TagCaracter(nome=b'code', raiz=b'//error', opcoes=CONST.CODE.opcoes.keys())
        self.message = TagCaracter(nome=b'message', raiz=b'//error')

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<error>'
        xml += self.code.xml
        xml += self.message.xml
        xml += b'</error>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.code.xml = arquivo
            self.message.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.code.alertas)
        alertas.extend(self.message.alertas)
        return alertas

    alertas = property(get_alertas)


class ClassePagamentoErros(XMLAPI):

    def __init__(self):
        super(ClassePagamentoErros, self).__init__()
        self.errors = []

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<errors>'
        for erro in self.errors:
            xml += erro.xml

        xml += b'</errors>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.errors = self.le_grupo(b'//errors/error', Error)

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        for error in self.errors:
            alertas.extend(error.alertas)

        return alertas

    alertas = property(get_alertas)
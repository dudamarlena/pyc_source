# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\assinatura\v2\classes\cancelamento.py
# Compiled at: 2015-12-29 19:37:23
from __future__ import division, print_function, unicode_literals
from ....core.base_classes import ABERTURA, TagCaracter, TagDataHoraUTC, XMLAPI
from ....core import CONST as CONST_BASE

class CONST(CONST_BASE):

    class STATUS(object):
        """
        Usado nas mensagens de RETORNO, vem embutido na tag 'status' com outros textos
        """
        PENDING = b'PENDING'
        ACTIVE = b'ACTIVE'
        CANCELLED = b'CANCELLED'
        CANCELLED_BY_RECEIVER = b'CANCELLED_BY_RECEIVER'
        CANCELLED_BY_SENDER = b'CANCELLED_BY_SENDER'
        EXPIRED = b'EXPIRED'
        OK = b'OK'
        opcoes = {PENDING: b'Assinatura pendente. Aguardando confimação pela operadora', 
           ACTIVE: b'Assinatura paga e confirmada pela operadora', 
           CANCELLED: b'Assinatura cancelada por não aprovação da PagSeguro u pela operadora', 
           CANCELLED_BY_RECEIVER: b'Assinatura cancelada por solicitação do vendedor', 
           CANCELLED_BY_SENDER: b'Assinatura cancelada por solicitação do comprador', 
           EXPIRED: b'Assinatura expirou', 
           OK: b'Assinatura cancelada'}


class ClasseCancelamentoAssinaturaRetorno(XMLAPI):

    def __init__(self):
        super(ClasseCancelamentoAssinaturaRetorno, self).__init__()
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//result')
        self.status = TagCaracter(nome=b'status', raiz=b'//result')

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<result>'
        xml += self.date.xml
        xml += self.status.xml
        xml += b'</result>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.date.xml = arquivo
            self.status.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.date.alertas)
        alertas.extend(self.status.alertas)
        return alertas

    alertas = property(get_alertas)
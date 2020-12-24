# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\assinatura\v2\classes\consulta.py
# Compiled at: 2015-12-29 16:38:09
from __future__ import division, print_function, unicode_literals
from ....core.base_classes import ABERTURA, TagCaracter, TagInteiro, TagDataHoraUTC, TagDecimal, XMLAPI

class CONST(object):

    class STATUS(object):
        INITIATED = b'INITIATED'
        PENDING = b'PENDING'
        ACTIVE = b'ACTIVE'
        CANCELLED = b'CANCELLED'
        CANCELLED_BY_RECEIVER = b'CANCELLED_BY_RECEIVER'
        CANCELLED_BY_SENDER = b'CANCELLED_BY_SENDER'
        EXPIRED = b'EXPIRED'
        opcoes = {INITIATED: b'Processo de assinatura iniciada', 
           PENDING: b'Assinatura pendente. Aguardando confimação pela operadora', 
           ACTIVE: b'Assinatura paga e confirmada pela operadora', 
           CANCELLED: b'Assinatura cancelada por não aprovação da PagSeguro u pela operadora', 
           CANCELLED_BY_RECEIVER: b'Assinatura cancelada por solicitação do vendedor', 
           CANCELLED_BY_SENDER: b'Assinatura cancelada por solicitação do comprador', 
           EXPIRED: b'Assinatura expirou'}

    class CHARGE(object):
        AUTO = b'auto'
        MANUAL = b'manual'
        opcoes = {AUTO: b'Cobrado automaticamente pela PagSeguro', 
           MANUAL: b'Cobrado manualmente pele vendedor', 
           b'AUTO': b'Cobrado automaticamente pela PagSeguro', 
           b'MANUAL': b'Cobrado manualmente pele vendedor'}


class Address(XMLAPI):

    def __init__(self):
        super(Address, self).__init__()
        self.country = TagCaracter(nome=b'country', raiz=b'//preApproval/sender/address', opcoes=('BRA', ), valor=b'BRA', obrigatorio=False)
        self.state = TagCaracter(nome=b'state', raiz=b'//preApproval/sender/address', tamanho_min=2, tamanho_max=2, obrigatorio=False)
        self.city = TagCaracter(nome=b'city', raiz=b'//preApproval/sender/address', obrigatorio=False, tamanho_min=2, tamanho_max=60)
        self.postalCode = TagCaracter(nome=b'postalCode', raiz=b'//preApproval/sender/address', tamanho_min=8, tamanho_max=8, obrigatorio=False)
        self.district = TagCaracter(nome=b'district', raiz=b'//preApproval/sender/address', obrigatorio=False, tamanho_max=60)
        self.street = TagCaracter(nome=b'street', raiz=b'//preApproval/sender/address', obrigatorio=False, tamanho_max=80)
        self.number = TagCaracter(nome=b'number', raiz=b'//preApproval/sender/address', obrigatorio=False, tamanho_max=20)
        self.complement = TagCaracter(nome=b'complement', raiz=b'//preApproval/sender/address', obrigatorio=False, tamanho_max=40)

    def get_xml(self):
        if not (self.country.valor or self.state.valor or self.city.valor or self.postalCode.valor or self.district.valor or self.street.valor or self.number.valor or self.complement.valor):
            return b''
        xml = XMLAPI.get_xml(self)
        xml += b'<address>'
        xml += self.country.xml
        xml += self.state.xml
        xml += self.city.xml
        xml += self.postalCode.xml
        xml += self.district.xml
        xml += self.street.xml
        xml += self.number.xml
        xml += self.complement.xml
        xml += b'</address>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.country.xml = arquivo
            self.state.xml = arquivo
            self.city.xml = arquivo
            self.postalCode.xml = arquivo
            self.district.xml = arquivo
            self.street.xml = arquivo
            self.number.xml = arquivo
            self.complement.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.country.alertas)
        alertas.extend(self.state.alertas)
        alertas.extend(self.city.alertas)
        alertas.extend(self.postalCode.alertas)
        alertas.extend(self.district.alertas)
        alertas.extend(self.street.alertas)
        alertas.extend(self.number.alertas)
        alertas.extend(self.complement.alertas)
        return alertas

    alertas = property(get_alertas)


class Phone(XMLAPI):

    def __init__(self):
        super(Phone, self).__init__()
        self.areaCode = TagInteiro(nome=b'areaCode', raiz=b'//preApproval/sender/phone', tamanho_min=2, tamanho_max=2, obrigatorio=False)
        self.number = TagInteiro(nome=b'number', raiz=b'//preApproval/sender/phone', tamanho_min=7, tamanho_max=9, obrigatorio=False)

    def get_xml(self):
        if not self.areaCode.valor and not self.number.valor:
            return b''
        xml = XMLAPI.get_xml(self)
        xml += b'<phone>'
        xml += self.areaCode.xml
        xml += self.number.xml
        xml += b'</phone>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.areaCode.xml = arquivo
            self.number.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.areaCode.alertas)
        alertas.extend(self.number.alertas)
        return alertas

    alertas = property(get_alertas)


class Sender(XMLAPI):

    def __init__(self):
        super(Sender, self).__init__()
        self.name = TagCaracter(nome=b'name', raiz=b'//preApproval/sender', tamanho_max=50, obrigatorio=False)
        self.email = TagCaracter(nome=b'email', raiz=b'//preApproval/sender', tamanho_max=60, obrigatorio=False)
        self.phone = Phone()
        self.address = Address()

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<sender>'
        xml += self.email.xml
        xml += self.name.xml
        xml += self.phone.xml
        xml += self.address.xml
        xml += b'</sender>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.email.xml = arquivo
            self.name.xml = arquivo
            self.phone.xml = arquivo
            self.address.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.email.alertas)
        alertas.extend(self.name.alertas)
        alertas.extend(self.phone.alertas)
        alertas.extend(self.address.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseConsultaAssinaturaResposta(XMLAPI):

    def __init__(self):
        super(ClasseConsultaAssinaturaResposta, self).__init__()
        self.name = TagCaracter(nome=b'name', raiz=b'//preApproval')
        self.code = TagCaracter(nome=b'code', raiz=b'//preApproval')
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//preApproval')
        self.tracker = TagCaracter(nome=b'tracker', raiz=b'//preApproval')
        self.status = TagCaracter(nome=b'status', raiz=b'//preApproval', opcoes=CONST.STATUS.opcoes.keys())
        self.reference = TagCaracter(nome=b'reference', raiz=b'//preApproval')
        self.lastEventDate = TagDataHoraUTC(nome=b'lastEventDate', raiz=b'//preApproval')
        self.charge = TagCaracter(nome=b'charge', raiz=b'//preApproval', opcoes=CONST.CHARGE.opcoes.keys())
        self.sender = Sender()

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<preApproval>'
        xml += self.name.xml
        xml += self.code.xml
        xml += self.date.xml
        xml += self.tracker.xml
        xml += self.status.xml
        xml += self.reference.xml
        xml += self.lastEventDate.xml
        xml += self.charge.xml
        xml += self.sender.xml
        xml += b'</preApproval>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.name.xml = arquivo
            self.code.xml = arquivo
            self.date.xml = arquivo
            self.tracker.xml = arquivo
            self.status.xml = arquivo
            self.reference.xml = arquivo
            self.lastEventDate.xml = arquivo
            self.charge.xml = arquivo
            self.sender.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.name.alertas)
        alertas.extend(self.code.alertas)
        alertas.extend(self.date.alertas)
        alertas.extend(self.tracker.alertas)
        alertas.extend(self.status.alertas)
        alertas.extend(self.reference.alertas)
        alertas.extend(self.lastEventDate.alertas)
        alertas.extend(self.charge.alertas)
        alertas.extend(self.sender.alertas)
        return alertas

    alertas = property(get_alertas)


class PreApproval(XMLAPI):

    def __init__(self):
        super(PreApproval, self).__init__()
        self.name = TagCaracter(nome=b'name', raiz=b'//preApproval')
        self.code = TagCaracter(nome=b'code', raiz=b'//preApproval')
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//preApproval')
        self.tracker = TagCaracter(nome=b'tracker', raiz=b'//preApproval')
        self.status = TagCaracter(nome=b'status', raiz=b'//preApproval', opcoes=CONST.STATUS.opcoes.keys())
        self.reference = TagCaracter(nome=b'reference', raiz=b'//preApproval')
        self.lastEventDate = TagDataHoraUTC(nome=b'lastEventDate', raiz=b'//preApproval')
        self.charge = TagCaracter(nome=b'charge', raiz=b'//preApproval', opcoes=CONST.CHARGE.opcoes.keys())

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<preApproval>'
        xml += self.name.xml
        xml += self.code.xml
        xml += self.date.xml
        xml += self.tracker.xml
        xml += self.status.xml
        xml += self.reference.xml
        xml += self.lastEventDate.xml
        xml += self.charge.xml
        xml += b'</phone>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.name.xml = arquivo
            self.code.xml = arquivo
            self.date.xml = arquivo
            self.tracker.xml = arquivo
            self.status.xml = arquivo
            self.reference.xml = arquivo
            self.lastEventDate.xml = arquivo
            self.charge.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.name.alertas)
        alertas.extend(self.code.alertas)
        alertas.extend(self.date.alertas)
        alertas.extend(self.tracker.alertas)
        alertas.extend(self.status.alertas)
        alertas.extend(self.reference.alertas)
        alertas.extend(self.lastEventDate.alertas)
        alertas.extend(self.charge.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseConsultaAssinaturasResposta(XMLAPI):

    def __init__(self):
        super(ClasseConsultaAssinaturasResposta, self).__init__()
        self.resultsInThisPage = TagInteiro(nome=b'resultsInThisPage', raiz=b'//preApprovalSearchResult')
        self.currentPage = TagInteiro(nome=b'currentPage', raiz=b'//preApprovalSearchResult')
        self.totalPages = TagInteiro(nome=b'totalPages', raiz=b'//preApprovalSearchResult')
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//preApprovalSearchResult')
        self.preApprovals = []

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<preApprovalSearchResult>'
        xml += self.resultsInThisPage.xml
        xml += self.currentPage.xml
        xml += self.totalPages.xml
        xml += self.date.xml
        for preApproval in self.preApprovals:
            xml += preApproval.xml

        xml += b'</preApprovalSearchResult>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.resultsInThisPage.xml = arquivo
            self.currentPage.xml = arquivo
            self.totalPages.xml = arquivo
            self.date.xml = arquivo
            self.preApprovals = self.le_grupo(b'//preApprovalSearchResult/preApprovals/preApproval', PreApproval)

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.resultsInThisPage.alertas)
        alertas.extend(self.currentPage.alertas)
        alertas.extend(self.totalPages.alertas)
        alertas.extend(self.date.alertas)
        for alerta in self.preApprovals:
            alertas.extend(alerta.alertas)

        return alertas

    alertas = property(get_alertas)
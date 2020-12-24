# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\assinatura\v2\classes\requisicao.py
# Compiled at: 2015-12-29 16:38:09
from __future__ import division, print_function, unicode_literals
from ....core.base_classes import ABERTURA, TagCaracter, TagInteiro, TagDataHoraUTC, TagDecimal, XMLAPI

class CONST(object):

    class PREAPPROVAL(object):

        class CHARGE(object):
            AUTO = b'auto'
            MANUAL = b'manual'
            opcoes = {AUTO: b'Automático (PagSeguro gerencia)', 
               MANUAL: b'Manual (Vendedor gerencia)'}

        class PERIOD(object):
            WEEKLY = b'WEEKLY'
            MONTHLY = b'MONTHLY'
            BIMONTHLY = b'BIMONTHLY'
            TRIMONTHLY = b'TRIMONTHLY'
            SEMIANNUALLY = b'SEMIANNUALLY'
            YEARLY = b'YEARLY'
            opcoes = {WEEKLY: b'Semanal', 
               MONTHLY: b'Mensal', 
               BIMONTHLY: b'Bimestral', 
               TRIMONTHLY: b'Trimestral', 
               SEMIANNUALLY: b'Semestral', 
               YEARLY: b'Anual'}


class Address(XMLAPI):

    def __init__(self):
        super(Address, self).__init__()
        self.country = TagCaracter(nome=b'country', raiz=b'//preApprovalRequest/sender/address', opcoes=('BRA', ), valor=b'BRA', obrigatorio=False)
        self.state = TagCaracter(nome=b'state', raiz=b'//preApprovalRequest/sender/address', tamanho_min=2, tamanho_max=2, obrigatorio=False)
        self.city = TagCaracter(nome=b'city', raiz=b'//preApprovalRequest/sender/address', obrigatorio=False, tamanho_min=2, tamanho_max=60)
        self.postalCode = TagCaracter(nome=b'postalCode', raiz=b'//preApprovalRequest/sender/address', tamanho_min=8, tamanho_max=8, obrigatorio=False)
        self.district = TagCaracter(nome=b'district', raiz=b'//preApprovalRequest/sender/address', obrigatorio=False, tamanho_max=60)
        self.street = TagCaracter(nome=b'street', raiz=b'//preApprovalRequest/sender/address', obrigatorio=False, tamanho_max=80)
        self.number = TagCaracter(nome=b'number', raiz=b'//preApprovalRequest/sender/address', obrigatorio=False, tamanho_max=20)
        self.complement = TagCaracter(nome=b'complement', raiz=b'//preApprovalRequest/sender/address', obrigatorio=False, tamanho_max=40)

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
        self.areaCode = TagInteiro(nome=b'areaCode', raiz=b'//preApprovalRequest/sender/phone', tamanho_min=2, tamanho_max=2, obrigatorio=False)
        self.number = TagInteiro(nome=b'number', raiz=b'//preApprovalRequest/sender/phone', tamanho_min=7, tamanho_max=9, obrigatorio=False)

    def get_xml(self):
        if not self.areaCode.valor and not self.number.valor:
            return b''
        xml = XMLAPI.get_xml(self)
        xml += b'<phone>'
        if self.areaCode.valor:
            xml += self.areaCode.xml
        if self.number.valor:
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
        self.name = TagCaracter(nome=b'name', raiz=b'//preApprovalRequest/sender', tamanho_max=50, obrigatorio=False)
        self.email = TagCaracter(nome=b'email', raiz=b'//preApprovalRequest/sender', tamanho_max=60, obrigatorio=False)
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


class PreApproval(XMLAPI):

    def __init__(self):
        super(PreApproval, self).__init__()
        self.charge = TagCaracter(nome=b'charge', raiz=b'//preApprovalRequest/preApproval', obrigatorio=False, opcoes=CONST.PREAPPROVAL.CHARGE.opcoes.keys(), valor=CONST.PREAPPROVAL.CHARGE.AUTO)
        self.name = TagCaracter(nome=b'name', raiz=b'//preApprovalRequest/preApproval', tamanho_max=100)
        self.details = TagCaracter(nome=b'details', raiz=b'//preApprovalRequest/preApproval', obrigatorio=False, tamanho_max=255)
        self.amountPerPayment = TagDecimal(nome=b'amountPerPayment', raiz=b'//preApprovalRequest/preApproval', tamanho_max=6, decimal_digitos=2, valor=0)
        self.maxAmountPerPayment = TagDecimal(nome=b'maxAmountPerPayment', raiz=b'//preApprovalRequest/preApproval', tamanho_max=6, decimal_digitos=2, valor=0, obrigatorio=False)
        self.period = TagCaracter(nome=b'period', raiz=b'//preApprovalRequest/preApproval', opcoes=CONST.PREAPPROVAL.PERIOD.opcoes.keys())
        self.finalDate = TagDataHoraUTC(nome=b'finalDate', raiz=b'//preApprovalRequest/preApproval')
        self.maxTotalAmount = TagDecimal(nome=b'maxTotalAmount', raiz=b'//preApprovalRequest/preApproval', tamanho_max=7, decimal_digitos=2)

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<preApproval>'
        xml += self.charge.xml
        xml += self.name.xml
        xml += self.details.xml
        if self.charge.valor == CONST.PREAPPROVAL.CHARGE.AUTO:
            xml += self.amountPerPayment.xml
        elif not self.amountPerPayment.valor:
            xml += self.maxAmountPerPayment.xml
        xml += self.period.xml
        xml += self.finalDate.xml
        xml += self.maxTotalAmount.xml
        xml += b'</preApproval>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.charge.xml = arquivo
            self.name.xml = arquivo
            self.details.xml = arquivo
            self.amountPerPayment.xml = arquivo
            self.maxAmountPerPayment.xml = arquivo
            self.period.xml = arquivo
            self.finalDate.xml = arquivo
            self.maxTotalAmount.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.charge.alertas)
        alertas.extend(self.name.alertas)
        alertas.extend(self.details.alertas)
        if self.charge.valor == CONST.PREAPPROVAL.CHARGE.AUTO:
            alertas.extend(self.amountPerPayment.alertas)
        elif not self.amountPerPayment.valor:
            alertas.extend(self.maxAmountPerPayment.alertas)
        alertas.extend(self.period.alertas)
        alertas.extend(self.finalDate.alertas)
        alertas.extend(self.maxTotalAmount.alertas)
        return alertas

    alertas = property(get_alertas)


class Receiver(XMLAPI):

    def __init__(self):
        super(Receiver, self).__init__()
        self.email = TagCaracter(nome=b'email', raiz=b'//preApprovalRequest/receiver', tamanho_max=60, obrigatorio=False)

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        if not self.email.valor:
            return b''
        xml += b'<receiver>'
        xml += self.email.xml
        xml += b'</receiver>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.email.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.email.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseAssinaturaRequisicao(XMLAPI):

    def __init__(self):
        super(ClasseAssinaturaRequisicao, self).__init__()
        self.reviewURL = TagCaracter(nome=b'reviewURL', raiz=b'//preApprovalRequest', tamanho_max=255, obrigatorio=False)
        self.redirectURL = TagCaracter(nome=b'redirectURL', raiz=b'//preApprovalRequest', tamanho_max=255, obrigatorio=False)
        self.reference = TagCaracter(nome=b'reference', raiz=b'//preApprovalRequest', tamanho_max=200, obrigatorio=False)
        self.sender = Sender()
        self.preApproval = PreApproval()
        self.receiver = Receiver()

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<preApprovalRequest>'
        xml += self.reviewURL.xml
        xml += self.redirectURL.xml
        xml += self.reference.xml
        xml += self.sender.xml
        xml += self.preApproval.xml
        xml += self.receiver.xml
        xml += b'</preApprovalRequest>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.reviewURL.xml = arquivo
            self.redirectURL.xml = arquivo
            self.reference.xml = arquivo
            self.sender.xml = arquivo
            self.preApproval.xml = arquivo
            self.receiver.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.reviewURL.alertas)
        alertas.extend(self.redirectURL.alertas)
        alertas.extend(self.reference.alertas)
        alertas.extend(self.sender.alertas)
        alertas.extend(self.preApproval.alertas)
        alertas.extend(self.receiver.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseAssinaturaResposta(XMLAPI):

    def __init__(self):
        super(ClasseAssinaturaResposta, self).__init__()
        self.code = TagCaracter(nome=b'code', raiz=b'//preApprovalRequest', tamanho_min=32, tamanho_max=32)
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//preApprovalRequest')

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<preApprovalRequest>'
        xml += self.code.xml
        xml += self.date.xml
        xml += b'</preApprovalRequest>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.code.xml = arquivo
            self.date.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.code.alertas)
        alertas.extend(self.date.alertas)
        return alertas

    alertas = property(get_alertas)
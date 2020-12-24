# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\consultas\v2\classes\abandonadas.py
# Compiled at: 2015-12-29 16:38:09
from __future__ import division, print_function, unicode_literals
from pagseguro_xml.core.base_classes import ABERTURA, TagCaracter, TagInteiro, TagDataHoraUTC, TagDecimal, XMLAPI

class CONST(object):

    class TRANSACTION(object):

        class TYPE(object):
            PAGAMENTO = 1
            opcoes = {PAGAMENTO: b'A transação foi criada por um comprador fazendo um pagamento.', 
               2: b'Testes', 
               3: b'Testes', 
               4: b'Testes', 
               5: b'Testes', 
               6: b'Testes', 
               7: b'Testes', 
               8: b'Testes', 
               9: b'Testes', 
               10: b'Testes', 
               11: b'Testes'}


class Transaction(XMLAPI):

    def __init__(self):
        super(Transaction, self).__init__()
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//transaction')
        self.lastEventDate = TagDataHoraUTC(nome=b'lastEventDate', raiz=b'//transaction')
        self.code = TagCaracter(nome=b'code', raiz=b'//transaction', tamanho_min=36, tamanho_max=36)
        self.reference = TagCaracter(nome=b'reference', raiz=b'//transaction', tamanho_max=200, obrigatorio=False)
        self.type = TagInteiro(nome=b'type', raiz=b'//transaction', opcoes=CONST.TRANSACTION.TYPE.opcoes.keys())
        self.grossAmount = TagDecimal(nome=b'grossAmount', raiz=b'//transaction', tamanho_max=10, decimal_digitos=2, valor=0)

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<transaction>'
        xml += self.date.xml
        xml += self.lastEventDate.xml
        xml += self.code.xml
        xml += self.reference.xml
        xml += self.type.xml
        xml += self.grossAmount.xml
        xml += b'</transaction>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.date.xml = arquivo
            self.lastEventDate.xml = arquivo
            self.code.xml = arquivo
            self.reference.xml = arquivo
            self.type.xml = arquivo
            self.grossAmount.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.date.alertas)
        alertas.extend(self.lastEventDate.alertas)
        alertas.extend(self.code.alertas)
        alertas.extend(self.reference.alertas)
        alertas.extend(self.type.alertas)
        alertas.extend(self.grossAmount.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseTransacaoAbandonadas(XMLAPI):

    def __init__(self):
        super(ClasseTransacaoAbandonadas, self).__init__()
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//transactionSearchResult')
        self.currentPage = TagInteiro(nome=b'currentPage', raiz=b'//transactionSearchResult', valor=1)
        self.resultsInThisPage = TagInteiro(nome=b'resultsInThisPage', raiz=b'//transactionSearchResult', valor=50)
        self.totalPages = TagInteiro(nome=b'totalPages', raiz=b'//transactionSearchResult')
        self.transactions = []

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += ABERTURA
        xml += b'<transactionSearchResult>'
        xml += self.date.xml
        xml += self.currentPage.xml
        xml += self.resultsInThisPage.xml
        xml += self.totalPages.xml
        xml += b'<transactions>'
        for transacao in self.transactions:
            xml += transacao.xml

        xml += b'</transactions>'
        xml += b'</transactionSearchResult>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.date.xml = arquivo
            self.currentPage.xml = arquivo
            self.resultsInThisPage.xml = arquivo
            self.totalPages.xml = arquivo
            self.transactions = self.le_grupo(b'//transactionSearchResult/transactions/transaction', Transaction)

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.date.alertas)
        alertas.extend(self.currentPage.alertas)
        alertas.extend(self.resultsInThisPage.alertas)
        alertas.extend(self.totalPages.alertas)
        for transaction in self.transactions:
            alertas.extend(transaction.alertas)

        return alertas

    alertas = property(get_alertas)
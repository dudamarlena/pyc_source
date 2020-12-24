# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\pagseguro_xml\consultas\v2\classes\historico.py
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

        class STATUS(object):
            AGUARDANDO_PAGAMENTO = 1
            EM_ANALISE = 2
            PAGA = 3
            DISPONIVEL = 4
            EM_DISPUTA = 5
            DEVOLVIDA = 6
            CANCELADA = 7
            CHARGEBACK_DEBITADO = 8
            EM_CONTENTACAO = 9
            opcoes = {AGUARDANDO_PAGAMENTO: b'Aguardando pagamento', 
               EM_ANALISE: b'Em análise', 
               PAGA: b'Paga', 
               DISPONIVEL: b'Disponível', 
               EM_DISPUTA: b'Em disputa', 
               DEVOLVIDA: b'Devolvida', 
               CANCELADA: b'Cancelada', 
               CHARGEBACK_DEBITADO: b'Chargeback debitado', 
               EM_CONTENTACAO: b'Em contestação'}
            desc = {AGUARDANDO_PAGAMENTO: b'o comprador iniciou a transação, mas até o momento o PagSeguro não recebeu nenhuma informação sobre o pagamento', 
               EM_ANALISE: b'o comprador optou por pagar com um cartão de crédito e o PagSeguro está analisando o risco da transação', 
               PAGA: b'a transação foi paga pelo comprador e o PagSeguro já recebeu uma confirmação da instituição financeira responsável pelo processamento', 
               DISPONIVEL: b'a transação foi paga e chegou ao final de seu prazo de liberação sem ter sido retornada e sem que haja nenhuma disputa aberta', 
               EM_DISPUTA: b'o comprador, dentro do prazo de liberação da transação, abriu uma disputa', 
               DEVOLVIDA: b'o valor da transação foi devolvido para o comprador', 
               CANCELADA: b'a transação foi cancelada sem ter sido finalizada', 
               CHARGEBACK_DEBITADO: b'o valor da transação foi devolvido para o comprador', 
               EM_CONTENTACAO: b'o comprador abriu uma solicitação de chargeback junto à operadora do cartão de crédito'}

        class CANCELLATIONSOURCE(object):
            INTERNAL = b'INTERNAL'
            EXTERNAL = b'EXTERNAL'
            opcoes = {INTERNAL: b'PagSeguro', 
               EXTERNAL: b'Intituições Financeiras'}

        class PAYMENTMETHOD(object):

            class TYPE(object):
                CARTAO_CREDITO = 1
                BOLETO = 2
                DEBITO_ONLINE = 3
                SALDO_PAGSEGURO = 4
                OI_PAGGO = 5
                DEPOSITO_CONTA = 7
                opcoes = {CARTAO_CREDITO: b'Cartão de crédito', 
                   BOLETO: b'Boleto', 
                   DEBITO_ONLINE: b'Débito online (TEF)', 
                   SALDO_PAGSEGURO: b'Saldo PagSeguro', 
                   OI_PAGGO: b'OI Paggo', 
                   DEPOSITO_CONTA: b'Depósito em conta'}


class PaymentMethod(XMLAPI):

    def __init__(self):
        super(PaymentMethod, self).__init__()
        self.type = TagInteiro(nome=b'type', raiz=b'//transaction/paymentMethod', opcoes=CONST.TRANSACTION.PAYMENTMETHOD.TYPE.opcoes)

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<paymentMethod>'
        xml += self.type.xml
        xml += b'</paymentMethod>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.type.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.type.alertas)
        return alertas

    alertas = property(get_alertas)


class Transaction(XMLAPI):

    def __init__(self):
        super(Transaction, self).__init__()
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//transaction')
        self.lastEventDate = TagDataHoraUTC(nome=b'lastEventDate', raiz=b'//transaction')
        self.code = TagCaracter(nome=b'code', raiz=b'//transaction', tamanho_min=36, tamanho_max=36)
        self.reference = TagCaracter(nome=b'reference', raiz=b'//transaction', tamanho_max=200, obrigatorio=False)
        self.type = TagInteiro(nome=b'type', raiz=b'//transaction', opcoes=CONST.TRANSACTION.TYPE.opcoes.keys())
        self.status = TagInteiro(nome=b'status', raiz=b'//transaction', opcoes=CONST.TRANSACTION.STATUS.opcoes.keys())
        self.cancellationSource = TagCaracter(nome=b'cancellationSource', raiz=b'//transaction', opcoes=CONST.TRANSACTION.CANCELLATIONSOURCE.opcoes.keys(), obrigatorio=False)
        self.paymentMethod = PaymentMethod()
        self.grossAmount = TagDecimal(nome=b'grossAmount', raiz=b'//transaction', tamanho_max=10, decimal_digitos=2, valor=0)
        self.discountAmount = TagDecimal(nome=b'discountAmount', raiz=b'//transaction', tamanho_max=10, decimal_digitos=2, valor=0)
        self.feeAmount = TagDecimal(nome=b'feeAmount', raiz=b'//transaction', tamanho_max=10, decimal_digitos=2, valor=0)
        self.netAmount = TagDecimal(nome=b'netAmount', raiz=b'//transaction', tamanho_max=10, decimal_digitos=2, valor=0)
        self.extraAmount = TagDecimal(nome=b'extraAmount', raiz=b'//transactionSearchResult', tamanho_max=10, decimal_digitos=2, valor=0, obrigatorio=False)

    def get_xml(self):
        xml = XMLAPI.get_xml(self)
        xml += b'<transaction>'
        xml += self.date.xml
        xml += self.lastEventDate.xml
        xml += self.code.xml
        xml += self.reference.xml
        xml += self.type.xml
        xml += self.status.xml
        xml += self.cancellationSource.xml
        xml += self.paymentMethod.xml
        xml += self.grossAmount.xml
        xml += self.discountAmount.xml
        xml += self.feeAmount.xml
        xml += self.netAmount.xml
        xml += self.extraAmount.xml
        xml += b'</transaction>'
        return xml

    def set_xml(self, arquivo):
        if self._le_xml(arquivo):
            self.date.xml = arquivo
            self.lastEventDate.xml = arquivo
            self.code.xml = arquivo
            self.reference.xml = arquivo
            self.type.xml = arquivo
            self.status.xml = arquivo
            self.cancellationSource.xml = arquivo
            self.paymentMethod.xml = arquivo
            self.grossAmount.xml = arquivo
            self.discountAmount.xml = arquivo
            self.feeAmount.xml = arquivo
            self.netAmount.xml = arquivo
            self.extraAmount.xml = arquivo

    xml = property(get_xml, set_xml)

    def get_alertas(self):
        alertas = []
        alertas.extend(self.date.alertas)
        alertas.extend(self.lastEventDate.alertas)
        alertas.extend(self.code.alertas)
        alertas.extend(self.reference.alertas)
        alertas.extend(self.type.alertas)
        alertas.extend(self.status.alertas)
        alertas.extend(self.cancellationSource.alertas)
        alertas.extend(self.paymentMethod.alertas)
        alertas.extend(self.grossAmount.alertas)
        alertas.extend(self.discountAmount.alertas)
        alertas.extend(self.feeAmount.alertas)
        alertas.extend(self.netAmount.alertas)
        alertas.extend(self.extraAmount.alertas)
        return alertas

    alertas = property(get_alertas)


class ClasseTransacaoHistorico(XMLAPI):

    def __init__(self):
        super(ClasseTransacaoHistorico, self).__init__()
        self.date = TagDataHoraUTC(nome=b'date', raiz=b'//transactionSearchResult')
        self.currentPage = TagInteiro(nome=b'currentPage', raiz=b'//transactionSearchResult', valor=1)
        self.resultsInThisPage = TagInteiro(nome=b'resultsInThisPage', raiz=b'//transactionSearchResult')
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
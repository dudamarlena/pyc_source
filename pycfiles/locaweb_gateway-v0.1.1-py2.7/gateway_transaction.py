# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/locaweb_gateway/gateway_transaction.py
# Compiled at: 2012-05-11 18:17:58


class GatewayTransaction(object):

    def __init__(self):
        self.id = None
        self.status = None
        self.url_acesso = None
        self.meio_pagamento = None
        self.numero_pedido = None
        self.detalhes = None
        self.erro = None
        self.erro_codigo = None
        self.erro_mensagem = None
        return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/locaweb_gateway/locaweb_gateway.py
# Compiled at: 2012-05-11 18:17:58
from gateway_http import GatewayRequest, GatewayResponse

class LocawebGatewayConfig(object):

    @classmethod
    def base_endpoint(cls):
        if cls.environment == 'production':
            endpoint = 'https://api.gatewaylocaweb.com.br/v1/transacao'
        else:
            endpoint = 'https://api-sandbox.gatewaylocaweb.com.br/v1/transacao'
        return endpoint


LocawebGatewayConfig.environment = 'production'
LocawebGatewayConfig.token = ''

class LocawebGateway(object):

    @classmethod
    def criar(cls, params={}):
        request = GatewayRequest(LocawebGatewayConfig.base_endpoint(), action='/')
        response = GatewayResponse(response=request.post(cls.gateway_params(params)))
        return response.parse()

    @classmethod
    def consultar(cls, transaction_id):
        request = GatewayRequest(LocawebGatewayConfig.base_endpoint(), action='/' + str(transaction_id))
        response = GatewayResponse(response=request.get(cls.gateway_params()))
        return response.parse()

    @classmethod
    def capturar(cls, transaction_id):
        request = GatewayRequest(LocawebGatewayConfig.base_endpoint(), action='/' + str(transaction_id) + '/capturar')
        response = GatewayResponse(response=request.post(cls.gateway_params()))
        return response.parse()

    @classmethod
    def cancelar(cls, transaction_id):
        request = GatewayRequest(LocawebGatewayConfig.base_endpoint(), action='/' + str(transaction_id) + '/estornar')
        response = GatewayResponse(response=request.post(cls.gateway_params()))
        return response.parse()

    @classmethod
    def gateway_params(cls, params={}):
        if params.__len__() == 0:
            request_params = {}
        else:
            request_params = {'transacao': params}
        request_params.update({'token': LocawebGatewayConfig.token})
        return request_params
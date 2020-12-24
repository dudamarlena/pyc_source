# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/sphirewallapi/sphirewall_api.py
# Compiled at: 2018-06-20 19:57:46
from sphirewallapi.sphirewall_api_firewall import FirewallSettings
from sphirewallapi.sphirewall_api_general import GeneralSettings
from sphirewallapi.sphirewall_api_network import NetworkSettings
from sphirewallapi.sphirewall_connection import SphirewallSocketTransportProvider
import uuid
try:
    import ujson as json
except ImportError:
    try:
        import simplejson as json
    except ImportError:
        import json

class SessionTimeoutException(Exception):

    def __init__(self, message):
        self.message = message


class MethodNotFoundException(Exception):

    def __init__(self, message):
        self.message = message


class MissingParamException(Exception):

    def __init__(self, message):
        self.message = message


class TransportProviderException(Exception):

    def __init__(self, message):
        self.message = message


class GeneralApplicationException(Exception):

    def __init__(self, message):
        self.message = message


DELEGATE_NOT_FOUND_ERRCODE = -1
AUTHENTICATION_ERROR_ERRCODE = -2
SERVICE_NOT_AVAILABLE_ERRCODE = -3
PARSING_ERROR_ERRCODE = -4
DELEGATE_GENERAL_ERROR_ERRCODE = -5

class SphirewallClientConnectionWrapper:

    def __init__(self, transport_handler):
        self.transport_handler = transport_handler
        self.token = None
        self.ignore_missing = False
        return

    def authenticate(self, username, password):
        response = self.transport_handler.send({'request': 'auth', 'username': username, 'password': password})
        jresponse = json.loads(response)
        if jresponse['code'] == 0:
            self.token = jresponse['token']
            return self.token

    def request(self, type, args):
        req = {'request': type, 'token': self.token, 'args': args}
        try:
            response = self.transport_handler.send(req)
        except Exception as e:
            raise TransportProviderException('Could not make a connection to the device.')

        return self.handle_response(response)

    def handle_response(self, response_data):
        json_loads = json.loads(response_data)
        response_code = json_loads['code']
        if response_code < 0:
            if response_code == DELEGATE_NOT_FOUND_ERRCODE:
                if not self.ignore_missing:
                    raise MethodNotFoundException(json_loads['message'])
                else:
                    return {}
            if response_code == AUTHENTICATION_ERROR_ERRCODE:
                raise SessionTimeoutException(json_loads['message'])
            if response_code == PARSING_ERROR_ERRCODE:
                raise MissingParamException(json_loads['message'])
            if response_code == DELEGATE_GENERAL_ERROR_ERRCODE:
                raise GeneralApplicationException(json_loads['message'])
        if 'response' in json_loads and 'err' in json_loads['response']:
            raise GeneralApplicationException(json_loads['response']['err'])
        return json_loads['response']


class SphirewallClient:

    def __init__(self, transport_provider=None, access_token=None):
        self.connection = SphirewallClientConnectionWrapper(transport_provider)
        self.connection.token = access_token

    def version(self):
        return self.connection.request('general/version', None)

    def info(self):
        return self.connection.request('general/info', None)

    def get_hostname(self):
        return self.hostname

    def get_port(self):
        return self.port

    def get_token(self):
        return self.connection.token

    def statistics_list(self, key, startDate, endDate):
        args = {'startDate': startDate, 
           'endDate': endDate, 
           'key': key}
        try:
            connection_request = self.connection.request('analytics/stats/metrics/get', args)
        except:
            return []

        if connection_request is not None:
            return connection_request['items']
        else:
            return []
            return

    def statistics_list_available(self):
        try:
            connection_request = self.connection.request('analytics/stats/metrics', {})
        except:
            return []

        if connection_request is not None:
            return connection_request['available']
        else:
            return []
            return

    def authenticate(self, username, password, ipaddress, mac, timeout=None, absolute_timeout=None, authentication_provider=None):
        args = {'username': username, 'password': password, 'ipaddress': ipaddress, 'mac': mac}
        if timeout:
            args['timeout'] = timeout
        if absolute_timeout:
            args['absoluteTimeout'] = absolute_timeout
        if authentication_provider:
            args['authentication_provider'] = authentication_provider
        response = self.connection.request('auth/login', args)
        return response

    def authenticate_mylinewize(self, username, password):
        args = {'username': username, 'password': password}
        response = self.connection.request('auth/mylinewize_login', args)
        return response

    def general(self):
        return GeneralSettings(self.connection)

    def firewall(self):
        return FirewallSettings(self.connection)

    def network(self):
        return NetworkSettings(self.connection)
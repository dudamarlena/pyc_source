# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /root/bin/clients/oneqloud_client/client.py
# Compiled at: 2020-01-14 16:39:33
import grpc, json, time, requests
from . import qbit_pb2_grpc
from future.utils import raise_from
import pkg_resources
from google.protobuf.json_format import MessageToDict
default_options = [
 ('grpc.max_send_message_length', -1),
 ('grpc.max_receive_message_length', -1),
 ('grpc.keepalive_timeout_ms', 2147483647),
 (
  'grpc.keepalive_permit_without_calls', True),
 ('grpc.http2.max_pings_without_data', 0),
 ('grpc.http2.min_ping_interval_without_data_ms', 300000)]

def create_get_auth(access_token):

    def get_auth_token(context, callback):
        callback([('authorization', access_token)], None)
        return

    return get_auth_token


class qloud_grpc_client(object):

    def __init__(self, auth_url, host, root_certs=None, client_id=None, client_secret=None):
        if not root_certs:
            root_certs = pkg_resources.resource_string('oneqloud_client', 'ca.pem')
        channel_creds = grpc.ssl_channel_credentials(root_certificates=root_certs)
        if client_id and client_secret:
            req_dict = {'client_id': client_id, 'client_secret': client_secret}
            try:
                response = requests.post(auth_url, json=req_dict)
                if response.ok:
                    response_data = response.json()
                    token = response_data['token']
                else:
                    raise Exception(response.reason + ' (' + str(response.status_code) + ')')
            except Exception as e:
                raise_from(type(e)('Authentication Request Failed', e), e)

            auth_creds = grpc.metadata_call_credentials(create_get_auth(token))
            channel_creds = grpc.composite_channel_credentials(channel_creds, auth_creds)
        self.channel = grpc.secure_channel(host, channel_creds, options=default_options)
        self.stub = qbit_pb2_grpc.QbitStub(self.channel)


class insecure_qloud_grpc_client(object):

    def __init__(self, host):
        self.channel = grpc.insecure_channel(host, options=default_options)
        self.stub = qbit_pb2_grpc.QbitStub(self.channel)


def client(root_certs=None, auth_url='https://portal-api.1qbit-prod.com/v1/get_project_token', host='grpc.1qbit-prod.com', client_id=None, client_secret=None, insecure=False):
    if insecure:
        return insecure_qloud_grpc_client(host).stub
    else:
        return qloud_grpc_client(auth_url, host, root_certs, client_id, client_secret).stub
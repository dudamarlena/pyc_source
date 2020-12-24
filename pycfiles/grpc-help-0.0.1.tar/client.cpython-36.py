# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/client.py
# Compiled at: 2018-12-26 05:17:11
# Size of source mod 2**32: 847 bytes
import socket, grpc
from grpc_help import interceptor
from grpc_help.key import read_public_key

def client_channel(address_port, ssl=False, **kwargs):
    if ssl:
        public_key_path = kwargs.get('public_key_path')
        assert public_key_path, 'certificate public_key_path can not be empty'
        trusted_certs = read_public_key(public_key_path)
        credentials = grpc.ssl_channel_credentials(root_certificates=trusted_certs)
        channel = grpc.secure_channel(address_port, credentials)
    else:
        channel = grpc.insecure_channel(address_port)
    hostname = socket.gethostname()
    ip = socket.gethostbyname(hostname)
    headers = (('host', hostname), ('ip', ip))
    header_adder_interceptor = (interceptor.header_adder_interceptor)(*headers)
    return grpc.intercept_channel(channel, header_adder_interceptor)
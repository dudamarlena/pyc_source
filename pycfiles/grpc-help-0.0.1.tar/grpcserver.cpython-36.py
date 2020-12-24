# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/caowenbin/xuetangx/grpc-help/grpc_help/grpcserver.py
# Compiled at: 2019-01-31 10:16:32
# Size of source mod 2**32: 2305 bytes
import sys
from importlib import import_module
import grpc, time, logging
from concurrent import futures
from grpc_help.autodiscover import discover_grpc_server, discover_grpc_class
from grpc_help.interceptor import RequestInterceptor
from grpc_help.key import read_private_key, read_public_key
logging.basicConfig()
logger = logging.getLogger(__name__)
_ONE_DAY_IN_SECONDS = 86400

def start(rpc_root_ruleconf, address_port=None, ssl=False, workers=4, interceptors=None, **kwargs):
    if interceptors is None:
        interceptors = (
         RequestInterceptor(),)
    elif isinstance(rpc_root_ruleconf, str):
        rpc_root_ruleconf = import_module(rpc_root_ruleconf)
    else:
        rpc_blueprint = getattr(rpc_root_ruleconf, 'rpc_blueprint', None)
        assert rpc_blueprint, 'not found rpc_blueprint'
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=workers), interceptors=interceptors)
        rpc_blueprint.register_server(server)
        address_port = address_port if address_port else '[::]:50051'
        if ssl:
            private_key_path = kwargs.get('private_key_path')
            public_key_path = kwargs.get('public_key_path')
            assert private_key_path and public_key_path, 'certificate private_key_path and public_key_path can not be empty'
            credentials = grpc.ssl_server_credentials((
             (
              read_private_key(private_key_path), read_public_key(public_key_path)),))
            server.add_secure_port(address_port, credentials)
        else:
            server.add_insecure_port(address_port)
        server.start()
        sys.stdout.write(f"Running GRPC server on {address_port} (Press CTRL+C to quit)\n")
        sys.stdout.flush()
        try:
            while True:
                time.sleep(_ONE_DAY_IN_SECONDS)

        except KeyboardInterrupt:
            server.stop(0)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/backend_client.py
# Compiled at: 2018-02-16 12:34:28
# Size of source mod 2**32: 415 bytes
from mercury_agent.configuration import get_configuration
from mercury.common.clients.rpc.backend import BackEndClient
__backend_client = None

def get_backend_client():
    global __backend_client
    if not __backend_client:
        __backend_client = BackEndClient(get_configuration().agent.remote.backend_url)
    return __backend_client
# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_http_asyncore_server/patch_service_gateway.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Jan 25, 2013\n\n@package: ally http\n@copyright: 2011 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the setup patch when the server is run with ally core http.\n'
from ..ally_http import server_type
from ..ally_http.processor import headerDecodeRequest, contentLengthDecode
from .processor import asyncoreContent
from .server import SERVER_ASYNCORE
from ally.container import ioc
import logging
log = logging.getLogger(__name__)
try:
    from .. import ally_gateway
except ImportError:
    log.info('No gateway service available thus skip the patching specific for asyncore')
else:
    ally_gateway = ally_gateway
    from ..ally_gateway.processor import updateAssemblyForwardForExternal, server_provide_gateway, assemblyForward, externalForward, GATEWAY_EXTERNAL

    @ioc.after(updateAssemblyForwardForExternal)
    def updateAssemblyForwardForHTTPAsyncore():
        if server_type() == SERVER_ASYNCORE and server_provide_gateway() == GATEWAY_EXTERNAL:
            assemblyForward().add(headerDecodeRequest(), contentLengthDecode(), asyncoreContent(), before=externalForward())
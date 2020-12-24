# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/support_nocache.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Sep 13, 2012\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the no cache headers support for browsers like IE.\n'
from ..ally_http.processor import headerEncodeResponse
from .processor import assemblyResources
from .processor_error import assemblyErrorDelivery
from .support_ajax import updateAssemblyErrorForHTTPAjax, updateAssemblyResourcesForHTTPAjax
from ally.container import ioc
from ally.design.processor.handler import Handler
from ally.http.impl.processor.headers.set_fixed import HeaderSetEncodeHandler

@ioc.config
def no_cache() -> bool:
    """Indicates that the server should send headers indicating that no cache is available (for browsers like IE)"""
    return True


@ioc.config
def headers_no_cache() -> dict:
    """The headers required by browsers like IE so it will not use caching"""
    return {'Cache-Control': [
                       'no-cache'], 
     'Pragma': [
                'no-cache']}


@ioc.entity
def headerSetNoCache() -> Handler:
    b = HeaderSetEncodeHandler()
    b.headers = headers_no_cache()
    return b


@ioc.after(updateAssemblyResourcesForHTTPAjax)
def updateAssemblyResourcesForHTTPNoCache():
    if no_cache():
        assemblyResources().add(headerSetNoCache(), after=headerEncodeResponse())


@ioc.after(updateAssemblyErrorForHTTPAjax)
def updateAssemblyErrorForHTTPNoCache():
    if no_cache():
        assemblyErrorDelivery().add(headerSetNoCache(), after=headerEncodeResponse())
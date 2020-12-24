# uncompyle6 version 3.6.7
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/__setup__/ally_core_http/support_ajax.py
# Compiled at: 2013-10-02 09:54:40
__doc__ = '\nCreated on Nov 24, 2011\n\n@package: ally core http\n@copyright: 2012 Sourcefabric o.p.s.\n@license: http://www.gnu.org/licenses/gpl-3.0.txt\n@author: Gabriel Nistor\n\nProvides the javascript setup required by browser for ajax.\n'
from ..ally_http.processor import headerEncodeResponse
from .processor import updateAssemblyResources, assemblyResources
from ally.container import ioc
from ally.design.processor.handler import Handler
from ally.http.impl.processor.headers.set_fixed import HeaderSetEncodeHandler
from ally.http.impl.processor.method_deliver_ok import DeliverOkForMethodHandler
from ally.http.spec.server import HTTP_OPTIONS
from .processor_error import assemblyErrorDelivery, updateAssemblyErrorDelivery

@ioc.config
def ajax_cross_domain() -> bool:
    """Indicates that the server should also be able to support cross domain ajax requests"""
    return True


@ioc.config
def headers_ajax() -> dict:
    """The ajax specific headers required by browser for cross domain calls"""
    return {'Access-Control-Allow-Origin': [
                                     '*'], 
     'Access-Control-Allow-Headers': [
                                      'X-Filter', 'X-HTTP-Method-Override', 'X-Format-DateTime', 'Authorization',
                                      'X-CAPTCHA-Challenge', 'X-CAPTCHA-Response']}


@ioc.entity
def headerSetAjax() -> Handler:
    b = HeaderSetEncodeHandler()
    b.headers = headers_ajax()
    return b


@ioc.entity
def deliverOkForOptionsHandler() -> Handler:
    b = DeliverOkForMethodHandler()
    b.forMethod = HTTP_OPTIONS
    return b


@ioc.after(updateAssemblyResources)
def updateAssemblyResourcesForHTTPAjax():
    if ajax_cross_domain():
        assemblyResources().add(headerSetAjax(), deliverOkForOptionsHandler(), after=headerEncodeResponse())


@ioc.after(updateAssemblyErrorDelivery)
def updateAssemblyErrorForHTTPAjax():
    if ajax_cross_domain():
        assemblyErrorDelivery().add(headerSetAjax(), after=headerEncodeResponse())
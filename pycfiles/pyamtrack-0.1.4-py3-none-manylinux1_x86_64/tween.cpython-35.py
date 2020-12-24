# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_apm/tween.py
# Compiled at: 2020-01-13 08:58:45
# Size of source mod 2**32: 4590 bytes
__doc__ = 'PyAMS_apm.tween module\n\nThis module provides a custom tween which is used to integrate the Pyramid application\nwith APM, sending requests frames to the APM server.\n'
import sys, pkg_resources, elasticapm
from elasticapm.utils import compat, get_url_dict
from pyramid.compat import reraise
from pyramid.settings import asbool
__docformat__ = 'restructuredtext'

def list_from_setting(config, setting):
    """Split configuration setting"""
    value = config.get(setting)
    if not value:
        return
    return value.split()


def get_data_from_request(request):
    """Extract main APM data from request properties"""
    data = {'headers': dict(**request.headers), 
     'method': request.method, 
     'socket': {'remote_address': request.remote_addr, 
                'encrypted': request.scheme == 'https'}, 
     
     'cookies': dict(**request.cookies), 
     'url': get_url_dict(request.url)}
    data['headers'].pop('Cookie', None)
    return data


def get_data_from_response(response):
    """Extract APM data from response properties"""
    data = {'status_code': response.status_int}
    if response.headers:
        data['headers'] = {key:';'.join(response.headers.getall(key)) for key in compat.iterkeys(response.headers)}
    return data


class elastic_apm_tween_factory:
    """elastic_apm_tween_factory"""

    def __init__(self, handler, registry):
        self.handler = handler
        self.registry = registry
        config = registry.settings
        service_version = config.get('elasticapm.service_version')
        if service_version:
            try:
                service_version = pkg_resources.get_distribution(service_version).version
            except pkg_resources.DistributionNotFound:
                pass

        self.client = elasticapm.Client(server_url=config.get('elasticapm.server_url'), server_timeout=config.get('elasticapm.server_timeout'), name=config.get('elasticapm.name'), framework_name='Pyramid', framework_version=pkg_resources.get_distribution('pyramid').version, service_name=config.get('elasticapm.service_name'), service_version=service_version, secret_token=config.get('elasticapm.secret_token'), include_paths=list_from_setting(config, 'elasticapm.include_paths'), exclude_paths=list_from_setting(config, 'elasticapm.exclude_paths'), debug=asbool(config.get('elasticapm.debug')))

    def __call__(self, request):
        self.client.begin_transaction('request')
        try:
            try:
                response = self.handler(request)
                transaction_result = response.status[0] + 'xx'
                elasticapm.set_context(lambda : get_data_from_response(response), 'response')
                return response
            except Exception:
                transaction_result = '5xx'
                self.client.capture_exception(context={'request': get_data_from_request(request)}, handled=False)
                reraise(*sys.exc_info())

        finally:
            try:
                view_name = request.view_name
                if not view_name:
                    view_name = request.traversed[(-1)] if request.traversed else '/'
            except AttributeError:
                view_name = ''

            transaction_name = request.matched_route.pattern if request.matched_route else view_name
            transaction_name = ' '.join((request.method, transaction_name)) if transaction_name else ''
            elasticapm.set_context(lambda : get_data_from_request(request), 'request')
            self.client.end_transaction(transaction_name, transaction_result)
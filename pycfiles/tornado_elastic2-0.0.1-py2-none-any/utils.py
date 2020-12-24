# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: tornado_elastic/utils.py
# Compiled at: 2020-01-06 01:31:14
from elasticapm.utils import get_url_dict

def get_data_from_request(request):
    url = ('{}://{}{}').format(request.protocol, request.host, request.uri)
    data = {'headers': dict(**request.headers), 
       'method': request.method, 
       'socket': {'remote_address': request.remote_ip, 
                  'encrypted': request.protocol == 'https'}, 
       'cookies': dict(**request.cookies), 
       'url': get_url_dict(url), 
       'body': request.body}
    data['headers'].pop('Cookie', None)
    return data


def get_data_from_response(response):
    data = {'status_code': response.get_status()}
    if response._headers:
        data['headers'] = response._headers._dict
    return data
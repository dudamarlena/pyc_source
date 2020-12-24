# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mjumbewu/Programming/projects/django-proxy/proxy/views.py
# Compiled at: 2019-07-05 14:22:11
# Size of source mod 2**32: 4195 bytes
import re, requests
from django.http import HttpResponse
from django.http import QueryDict
try:
    from urlparse import urlparse
except:
    from urllib.parse import urlparse

def proxy_view(request, url, requests_args=None):
    """
    Forward as close to an exact copy of the request as possible along to the
    given url.  Respond with as close to an exact copy of the resulting
    response as possible.

    If there are any additional arguments you wish to send to requests, put
    them in the requests_args dictionary.
    """
    requests_args = (requests_args or {}).copy()
    headers = get_headers(request.META)
    params = request.GET.copy()
    if 'headers' not in requests_args:
        requests_args['headers'] = {}
    if 'data' not in requests_args:
        requests_args['data'] = request.body
    if 'params' not in requests_args:
        requests_args['params'] = QueryDict('', mutable=True)
    headers.update(requests_args['headers'])
    params.update(requests_args['params'])
    for key in list(headers.keys()):
        if key.lower() == 'content-length':
            del headers[key]

    requests_args['headers'] = headers
    requests_args['params'] = params
    response = (requests.request)((request.method), url, **requests_args)
    proxy_response = HttpResponse((response.content),
      status=(response.status_code))
    excluded_headers = set([
     'connection', 'keep-alive', 'proxy-authenticate',
     'proxy-authorization', 'te', 'trailers', 'transfer-encoding',
     'upgrade',
     'content-encoding',
     'content-length'])
    for key, value in response.headers.items():
        if key.lower() in excluded_headers:
            continue
        else:
            if key.lower() == 'location':
                proxy_response[key] = make_absolute_location(response.url, value)
            else:
                proxy_response[key] = value

    return proxy_response


def make_absolute_location(base_url, location):
    """
    Convert a location header into an absolute URL.
    """
    absolute_pattern = re.compile('^[a-zA-Z]+://.*$')
    if absolute_pattern.match(location):
        return location
    parsed_url = urlparse(base_url)
    if location.startswith('//'):
        return parsed_url.scheme + ':' + location
    else:
        if location.startswith('/'):
            return parsed_url.scheme + '://' + parsed_url.netloc + location
        else:
            return parsed_url.scheme + '://' + parsed_url.netloc + parsed_url.path.rsplit('/', 1)[0] + '/' + location
        return location


def get_headers(environ):
    """
    Retrieve the HTTP headers from a WSGI environment dictionary.  See
    https://docs.djangoproject.com/en/dev/ref/request-response/#django.http.HttpRequest.META
    """
    headers = {}
    for key, value in environ.items():
        if key.startswith('HTTP_') and key != 'HTTP_HOST':
            headers[key[5:].replace('_', '-')] = value
        else:
            if key in ('CONTENT_TYPE', 'CONTENT_LENGTH'):
                headers[key.replace('_', '-')] = value

    return headers
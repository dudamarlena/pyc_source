# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/http.py
# Compiled at: 2017-04-05 02:41:41
# Size of source mod 2**32: 1729 bytes
"""Helper module to perform HTTP requests with SPNEGO auth."""
import json, urllib.request, urllib.error, urllib.parse, urllib_kerberos

def create_http_opener(proxy=None):
    """Creates http opener with spnego handler."""
    https_support = urllib.request.HTTPSHandler(debuglevel=1)
    if not proxy:
        proxy = {}
    if proxy == 'ENV':
        proxy_support = urllib.request.ProxyHandler()
    else:
        proxy_support = urllib.request.ProxyHandler(proxy)
    krb_support = urllib_kerberos.HTTPKerberosAuthHandler(mutual=False)
    return urllib.request.build_opener(https_support, proxy_support, krb_support)


def make_request(url, method, data, headers=None):
    """Constructs http request."""
    request = urllib.request.Request(url)
    request.get_method = lambda : method.upper()
    if request.get_method() not in ('GET', 'DELETE'):
        if data is None:
            length = 0
        else:
            if not isinstance(data, str):
                payload = json.dumps(data)
            else:
                payload = data
            length = len(payload)
            request.data = payload
        request.add_header('Content-Length', str(length))
    if not headers:
        headers = []
    for header in headers:
        if len(header) == 2:
            key, value = header
            key.strip(' ')
            value.strip(' ')
        else:
            key = header[0]
            key.strip(' ')
            value = '1'
        request.add_header(key, value)

    return request
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/rensike/Workspace/icv/icv/utils/http.py
# Compiled at: 2019-07-26 07:35:56
# Size of source mod 2**32: 3110 bytes
from ..core.http.client.client import IcvHttpClient
from ..core.http.methods import HttpMethod
from .itis import is_dir, is_seq
from .codec import json_encode

def request(method, url, data=None, params=None, headers=None, timeout=3000):
    method = str(method).upper()
    if method == HttpMethod.POST:
        return do_post(url=url, data=data, params=params, headers=headers, timeout=timeout)
    if method == HttpMethod.GET:
        return do_get(url=url, params=params, headers=headers, timeout=timeout)
    if method == HttpMethod.PUT:
        return do_put(url=url, data=data, params=params, headers=headers, timeout=timeout)
    if method == HttpMethod.DELETE:
        return do_post(url=url, data=data, params=params, headers=headers, timeout=timeout)
    if method == HttpMethod.OPTIONS:
        return do_post(url=url, data=data, params=params, headers=headers, timeout=timeout)
    raise Exception('Request Method Is Not Support!')


def do_post(url, data=None, json=False, form=False, params=None, headers=None, timeout=3000):
    http_client = IcvHttpClient(url, data=data, params=params, headers=headers, timeout=timeout)
    return http_client.post(json=json, form=form)


def do_get(url, params=None, headers=None, timeout=3000):
    http_client = IcvHttpClient(url, params=params, headers=headers, timeout=timeout)
    return http_client.get()


def do_put(url, data=None, json=False, form=False, params=None, headers=None, timeout=3000):
    http_client = IcvHttpClient(url, data=data, params=params, headers=headers, timeout=timeout)
    return http_client.put(json=json, form=form)


def do_delete(url, data=None, params=None, headers=None, timeout=3000):
    http_client = IcvHttpClient(url, data=data, params=params, headers=headers, timeout=timeout)
    return http_client.delete()


def do_options(url, data=None, params=None, headers=None, timeout=3000):
    http_client = IcvHttpClient(url, data=data, params=params, headers=headers, timeout=timeout)
    return http_client.options()


def file_server(dir, port, url_path_prefix='', debug=False, include_sub=False):
    assert is_dir(dir)
    from bottle import static_file, Bottle
    app = Bottle()
    url_path = '/%s/:path#.+#' % url_path_prefix.strip('/') if include_sub else '/%s/:filename' % url_path_prefix.strip('/')
    app.route(url_path, HttpMethod.GET, lambda path: static_file(path, dir))
    app.run(host='0.0.0.0', port=port, debug=debug)


def simple(port, methods=None, debug=False):
    if not methods is None:
        if not is_seq(methods):
            assert len([m for m in methods if m not in HttpMethod.methods])
    if methods is None:
        methods = HttpMethod.methods
    from bottle import Bottle, request
    app = Bottle()

    def _handler(uri):
        return json_encode(dict(uri=uri,
          url_path=(request.url),
          url_query=(request.query.decode()),
          request_method=(request.method),
          request_data=(request.json),
          request_headers=(request.headers)))

    app.route(['/<uri:re:.+>', '/'], methods, _handler)
    app.run(host='0.0.0.0', port=port, debug=debug)
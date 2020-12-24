# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/http_fun.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import graph
from robograph.datamodel.nodes.lib import printer, value, http

def test_get_graph(url, query_params):
    http_params = dict(url=url, query=query_params, mime_type='application/json', verify_ssl=False)
    v = value.Value(value=url)
    h = http.Get(**http_params)
    p = printer.ConsolePrinter()
    g = graph.Graph('test_get_graph', [v, h, p])
    g.connect(p, h, 'message')
    g.connect(h, v, 'url')
    return g


def test_post_graph(url, post_data):
    http_params = dict(url=url, mime_type='application/json', verify_ssl=False)
    v = value.Value(value=url)
    post_data = value.Value(value=post_data)
    h = http.Post(**http_params)
    p = printer.ConsolePrinter()
    g = graph.Graph('test_post_graph', [v, post_data, h, p])
    g.connect(p, h, 'message')
    g.connect(h, v, 'url')
    g.connect(h, post_data, 'post_data')
    return g


def test_put_graph(url, put_data):
    http_params = dict(url=url, post_data=put_data, mime_type='application/json', verify_ssl=False)
    v = value.Value(value=url)
    h = http.Put(**http_params)
    p = printer.ConsolePrinter()
    g = graph.Graph('test_put_graph', [v, h, p])
    g.connect(p, h, 'message')
    g.connect(h, v, 'url')
    return g


def test_delete_graph(url):
    http_params = dict(url=url, mime_type='application/json', verify_ssl=False)
    v = value.Value(value=url)
    h = http.Delete(**http_params)
    p = printer.ConsolePrinter()
    g = graph.Graph('test_delete_graph', [v, h, p])
    g.connect(p, h, 'message')
    g.connect(h, v, 'url')
    return g
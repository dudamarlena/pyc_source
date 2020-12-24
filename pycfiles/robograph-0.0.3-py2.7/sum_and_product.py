# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/sum_and_product.py
# Compiled at: 2016-07-13 17:51:17
import logging
from robograph.datamodel.base import graph
from robograph.datamodel.nodes.lib import apply, printer, value, buffers

def sum_and_product(list_of_numbers):
    v = value.Value(value=list_of_numbers)
    s = apply.Apply(function=sum)
    m = apply.Apply(function=lambda c: reduce(lambda x, y: x * y, c))
    b = buffers.Buffer()
    p = printer.ConsolePrinter()
    g = graph.Graph('sum_and_product', [v, s, m, p, b])
    g.connect(p, b, 'message')
    g.connect(b, s, 'sum value')
    g.connect(b, m, 'product value')
    g.connect(s, v, 'argument')
    g.connect(m, v, 'argument')
    return g


def logged_sum_and_product(list_of_numbers):
    v = value.Value(value=list_of_numbers)
    s = apply.Apply(function=sum)
    m = apply.Apply(function=lambda c: reduce(lambda x, y: x * y, c))
    b = buffers.Buffer()
    logging.basicConfig(level=logging.ERROR)
    p = printer.LogPrinter(logger=logging.getLogger(__name__), loglevel=logging.ERROR)
    g = graph.Graph('logged_sum_and_product', [v, s, m, b, p])
    g.connect(p, b, 'message')
    g.connect(b, s, 'sum value')
    g.connect(b, m, 'product value')
    g.connect(s, v, 'argument')
    g.connect(m, v, 'argument')
    return g
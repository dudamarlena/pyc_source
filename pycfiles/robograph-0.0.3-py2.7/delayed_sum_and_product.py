# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/delayed_sum_and_product.py
# Compiled at: 2016-07-13 17:39:48
from datamodel.base import graph
from datamodel.nodes.lib import apply, printer, value, buffers

def delayed_sum_and_product(list_of_numbers, delay):
    val = value.Value(value=list_of_numbers)
    summer = apply.Apply(function=sum)
    multiplier = apply.Apply(function=lambda c: reduce(lambda x, y: x * y, c))
    delayed_value_buffer = buffers.DelayedBuffer(seconds=delay)
    printout = printer.ConsolePrinter()
    g = graph.Graph('sum_and_product', [val, summer, multiplier,
     printout, delayed_value_buffer,
     delayed_value_buffer])
    g.connect(printout, delayed_value_buffer, 'message')
    g.connect(delayed_value_buffer, summer, 'sum value')
    g.connect(delayed_value_buffer, multiplier, 'product value')
    g.connect(summer, val, 'argument')
    g.connect(multiplier, val, 'argument')
    return g
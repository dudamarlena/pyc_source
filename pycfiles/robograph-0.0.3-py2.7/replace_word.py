# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/replace_word.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import graph
from robograph.datamodel.nodes.lib import printer, branching, value

def replace_word(text):
    t = value.Value(value=text, name='text')
    s = branching.IfThenApply(condition=lambda x: 'hello' in x, function_true=lambda x: x.replace('hello', 'ciao'), function_false=lambda x: x.replace(' ', '_'), name='if')
    p = printer.ConsolePrinter()
    g = graph.Graph('replace_word', [t, s, p])
    g.connect(p, s, 'message')
    g.connect(s, t, 'data')
    return g
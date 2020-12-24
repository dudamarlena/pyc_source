# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sample_graphs/execution_stop.py
# Compiled at: 2016-07-13 17:17:02
from datamodel.base import graph, exceptions
from datamodel.nodes.lib import value
from robograph.datamodel.nodes.lib import apply

def execution_stop(number):

    def stop_here(value):
        if value >= 0:
            raise exceptions.StopGraphExecutionSignal('arg is positive')
        raise exceptions.StopGraphExecutionSignal('arg is negative')

    v = value.Value(value=number)
    a = apply.Apply(function=stop_here)
    g = graph.Graph('execution_stop', [a, v])
    g.connect(a, v, 'argument')
    return g
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/tests/test_serializer.py
# Compiled at: 2016-07-13 17:51:17
from robograph.datamodel.base import graph
from robograph.datamodel.nodes import serializer
from robograph.datamodel.nodes.lib import value, buffers, apply

def test_node_serializer():
    instance = apply.Apply(function=lambda x: x + 2, argument=3, name='test')
    serialized = serializer.NodeSerializer.serialize(instance)
    deserialized = serializer.NodeSerializer.deserialize(serialized)
    assert instance.name == deserialized.name
    assert instance.output_label == deserialized.output_label
    assert instance.output() == deserialized.output()


def test_graph_serializer():
    a = value.Value(value=1, name='val_a')
    b = value.Value(value=2, name='val_b')
    s = buffers.Buffer(name='buffer')
    g = graph.Graph('test', [a, b, s])
    g.connect(s, a, 'val_a')
    g.connect(s, b, 'val_b')
    serialized = serializer.GraphSerializer.serialize(g)
    deserialized = serializer.GraphSerializer.deserialize(serialized)
    assert g.name == deserialized.name
    assert g.nxgraph == g.nxgraph
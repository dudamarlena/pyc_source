# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/graph/connection.py
# Compiled at: 2020-05-01 08:37:22
# Size of source mod 2**32: 10089 bytes
"""
 Copyright (C) 2018-2020 Intel Corporation

 Licensed under the Apache License, Version 2.0 (the "License");
 you may not use this file except in compliance with the License.
 You may obtain a copy of the License at

      http://www.apache.org/licenses/LICENSE-2.0

 Unless required by applicable law or agreed to in writing, software
 distributed under the License is distributed on an "AS IS" BASIS,
 WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 See the License for the specific language governing permissions and
 limitations under the License.
"""
from collections import namedtuple
from copy import deepcopy
from mo.utils.error import Error

class Connection:

    def __init__(self, graph, source, destinations: list, control_flow=False):
        self.graph = graph
        self.source = source
        self.destinations = destinations
        self.control_flow = control_flow
        self.data = namedtuple('Data', ['get_value', 'get_shape'])
        self.data.get_value = self._get_value
        self.data.get_shape = self._get_shape

    def _get_value(self):
        if self.graph.stage == 'front':
            return
        return self.source.node.out_node((self.source.idx), control_flow=(self.control_flow)).value

    def _get_shape(self):
        if self.graph.stage == 'front':
            return
        return self.source.node.out_node((self.source.idx), control_flow=(self.control_flow)).shape

    def get_source(self):
        return self.source

    def get_destination(self):
        if self.destinations:
            if len(self.destinations) > 1:
                raise Error('Connection has more than one destination: {}'.format(len(self.destinations)))
        if self.destinations:
            return self.destinations[0]

    def get_destinations(self):
        return self.destinations

    def set_source(self, port):
        if port.type == 'in':
            raise Error("Wrong port type in set_source method. Should be 'out' but given 'in'")
        else:
            if self.control_flow is True:
                raise Error('Cannot operate with connection with control_flow=True')
            if self.graph.stage == 'front':
                scr_node = port.node
                for dst_port in self.destinations:
                    edge_attrs, u, v, key = dst_port.get_in_edge_attrs(data=True)
                    if u is not None:
                        edge_attrs['out'] = port.idx
                        self.graph.remove_edge(u, v, key=key)
                        (self.graph.add_edge)((scr_node.id), v, **edge_attrs)
                    else:
                        self.graph.create_edge(scr_node, dst_port.node, port.idx, dst_port.idx)

            else:
                port._create_data_if_necessary()
                port_out_data = port.node.out_node(port.idx)
                if self.source is not None:
                    if self.source.idx in self.source.node.out_nodes():
                        source_out_data = self.source.node.out_node(self.source.idx)
                        attrs = deepcopy(source_out_data.attrs())
                        if 'fw_tensor_debug_info' in source_out_data.attrs():
                            del self.graph.node[source_out_data.id]['fw_tensor_debug_info']
                        for attr in attrs:
                            port_out_data[attr] = attrs[attr]

                for dst_port in self.destinations:
                    edge_attrs, u, v, key = dst_port.get_in_edge_attrs(data=True)
                    if u is not None:
                        self.graph.remove_edge(u, v, key=key)
                        (self.graph.add_edge)((port_out_data.id), v, **edge_attrs)
                    else:
                        (self.graph.add_edge)((port_out_data.id), (dst_port.node.id), **{'in': dst_port.idx})

    def set_destination(self, port):

        def check_and_remove_edge():
            if self.destinations:
                for destination in self.destinations:
                    edge_attrs, u, v, key = destination.get_in_edge_attrs(data=True)
                    if u is None:
                        raise Error('Broken Connection object! Destination (node:{}) is not connected to source.'.format(destination.node.name))
                    destination.disconnect()
                    return edge_attrs

        if self.destinations:
            if len(self.destinations) > 1:
                raise Error('set_destination applicable only for connections that has exactly one destination or                          when there is no destinations')
        if port.type == 'out':
            raise Error("Wrong port type in set_destination method. Should be 'in' but given 'out'")
        if self.control_flow is True:
            raise Error('Cannot operate with connection with control_flow=True')
        if self.graph.stage == 'front':
            if self.source is not None:
                node = self.source.node
                check_and_remove_edge()
                self.graph.create_edge(node, (port.node), out_port=(self.source.idx), in_port=(port.idx))
            self.destinations = [
             port]
        else:
            if self.source is not None:
                data_node = self.source._create_data_if_necessary()
                edge_attrs = check_and_remove_edge() or {}
                edge_attrs.update({'in': port.idx})
                (self.graph.add_edge)((data_node.id), (port.node.id), **edge_attrs)
            self.destinations = [
             port]

    def add_destination(self, port):
        if self.control_flow is True:
            raise Error('Cannot operate with connection with control_flow=True')
        else:
            if self.source is None:
                raise Error('Can not add destination for connection without source port!')
            if self.graph.stage == 'front':
                node = self.source.node
                self.graph.create_edge(node, (port.node), out_port=(self.source.idx), in_port=(port.idx))
            else:
                data_node = self.source._create_data_if_necessary()
                (self.graph.add_edge)((data_node.id), (port.node.id), **{'in': port.idx})
        self.destinations.append(port)

    def remove(self):
        if self.destinations:
            for dst_port in self.destinations:
                dst_port.disconnect()

        self.source = None
        self.destinations = []

    def insert_node(self, new_node):
        assert len(new_node.out_ports()) == 1, 'The node {} has several output ports'.format(new_node.soft_get('name'))
        source_port = self.get_source()
        self.set_source(new_node.out_port(0))
        source_port.connect(new_node.in_port(0))
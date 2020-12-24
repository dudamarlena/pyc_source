# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/graphviz/dot_wrapper.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 9706 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import re
from vipe.pipeline.pipeline import NodeImportance, Pipeline
from vipe.graphviz.dot_builder import DotBuilder
from vipe.graphviz.ports_label_printer import PortsLabelPrinter, PortName

class DotBuilderWrapper:
    __doc__ = 'Wrapper for DotBuilder class.\n\n    It is an intermediate layer between the dot format and business logic.\n    It translates business-level node objects to concepts of the dot format.\n    '

    def __init__(self, importance_score_map, show_input_ports, show_output_ports, vertical_orientation=True):
        """Args:
            importance_score_map (ImportanceScoreMap):
            show_input_ports (bool):
            show_output_ports (bool):
            vertical_orientation (bool): True if the graph should be drawn
                from top to bottom, False if it should be drawn from left to
                right.
        """
        self._DotBuilderWrapper__b = DotBuilder(vertical_orientation)
        self._DotBuilderWrapper__e_reg = _EdgesRegister()
        self._DotBuilderWrapper__n_reg = _NodesRegister()
        self._DotBuilderWrapper__importance_score_map = importance_score_map
        self._DotBuilderWrapper__show_input_ports = show_input_ports
        self._DotBuilderWrapper__show_output_ports = show_output_ports

    def __map(self, name):
        return _NamesConverter.run(name)

    def add_node(self, name, node):
        """Args:
            name (string): name of the node
            node (vipe.pipeline.pipeline.Node): data about the node
        """
        if self._DotBuilderWrapper__n_reg.contains(name):
            raise Exception('More than two nodes with the same name (here: "{}") are not allowed'.format(name))
        color = self._DotBuilderWrapper__get_color(node.importance)
        if name in [Pipeline.get_input_node_name(),
         Pipeline.get_output_node_name()]:
            self._DotBuilderWrapper__n_reg.add(name, _NodeInfo(True, True))
            self._DotBuilderWrapper__add_advanced_node(name, node, True, True, color, 'folder')
            return
        importance_score = self._DotBuilderWrapper__importance_score_map.get_score(node.importance)
        if importance_score > -1:
            self._DotBuilderWrapper__n_reg.add(name, _NodeInfo(self._DotBuilderWrapper__show_input_ports, self._DotBuilderWrapper__show_output_ports))
            self._DotBuilderWrapper__add_advanced_node(name, node, self._DotBuilderWrapper__show_input_ports, self._DotBuilderWrapper__show_output_ports, color)
        else:
            self._DotBuilderWrapper__n_reg.add(name, _NodeInfo(False, False))
            if importance_score == -1:
                self._DotBuilderWrapper__b.add_node(self._DotBuilderWrapper__map(name), labels=[''], shape='box', width=0.2, height=0.2, color=color)
            elif importance_score < -1:
                self._DotBuilderWrapper__b.add_node(self._DotBuilderWrapper__map(name), labels=[''], shape='box', width=0.1, height=0.1, color=color)

    @staticmethod
    def __get_color(importance):
        color = 'white'
        if importance == NodeImportance.normal:
            color = 'cyan'
        elif importance == NodeImportance.low:
            color = 'lightcyan'
        return color

    def __add_advanced_node(self, node_name, node, show_input_ports, show_output_ports, color, shape=None):
        """
        Args:
            shape(string): shape of the node. If None, the default
                approach of deciding which shape is appropriate is used.
        """
        labels = [
         node_name, 'type={}'.format(node.type)]
        if show_input_ports or show_output_ports:
            input_ports = []
            if show_input_ports:
                input_ports = self._DotBuilderWrapper__port_labels_to_PortNames(node.input_ports.keys(), True)
            output_ports = []
            if show_output_ports:
                output_ports = self._DotBuilderWrapper__port_labels_to_PortNames(node.output_ports.keys(), False)
            labels = [PortsLabelPrinter().run(labels, input_ports, output_ports, color)]
            if shape is None:
                shape = 'none'
            self._DotBuilderWrapper__b.add_node(self._DotBuilderWrapper__map(node_name), labels=labels, shape=shape, use_raw_labels=True)
        else:
            if shape is None:
                shape = 'box'
            self._DotBuilderWrapper__b.add_node(self._DotBuilderWrapper__map(node_name), labels=labels, shape=shape, color=color)

    @staticmethod
    def __port_labels_to_PortNames(port_labels, are_input_ports):
        names = []
        for n in sorted(port_labels):
            internal_name = DotBuilderWrapper._DotBuilderWrapper__port_name_to_internal_name(n, are_input_ports)
            names.append(PortName(n, internal_name))

        return names

    @staticmethod
    def __port_name_to_internal_name(name, is_input_port):
        if name is None:
            return
        prefix = 'output_'
        if is_input_port:
            prefix = 'input_'
        return '{}{}'.format(prefix, name)

    def add_data_node(self, data_id):
        """Args:
            data_id (string): data ID
        """
        self._DotBuilderWrapper__b.add_node(self._DotBuilderWrapper__map(data_id), shape='point')

    def add_edge(self, start, end):
        """Add connection between two nodes.

        The name field of the DataAddress might be a name of a node or a
        data ID - in the latter case the address corresponds to data.
        The port field of the address might be set to `None`. It is
        always `None` if the address corresponds to data.

        Args:
            start (DataAddress): start of the connection
            end (DataAddress): end of the connection
        """
        start_output_port = None
        if self._DotBuilderWrapper__n_reg.contains(start.node):
            if self._DotBuilderWrapper__n_reg.get(start.node).has_visible_output_ports:
                start_output_port = start.port
        end_input_port = None
        if self._DotBuilderWrapper__n_reg.contains(end.node):
            if self._DotBuilderWrapper__n_reg.get(end.node).has_visible_input_ports:
                end_input_port = end.port
        if start_output_port is not None or end_input_port is not None:
            self._DotBuilderWrapper__b.add_edge(self._DotBuilderWrapper__map(start.node), self._DotBuilderWrapper__port_name_to_internal_name(start_output_port, False), self._DotBuilderWrapper__map(end.node), self._DotBuilderWrapper__port_name_to_internal_name(end_input_port, True))
        else:
            assert start_output_port is None
            if not end_input_port is None:
                raise AssertionError
        if not self._DotBuilderWrapper__e_reg.contains(start.node, end.node):
            self._DotBuilderWrapper__b.add_edge(self._DotBuilderWrapper__map(start.node), None, self._DotBuilderWrapper__map(end.node), None)
        if not self._DotBuilderWrapper__e_reg.contains(start.node, end.node):
            self._DotBuilderWrapper__e_reg.add(start.node, end.node)

    def get_result(self):
        """Return:
            string: resulting graph in dot format
        """
        return self._DotBuilderWrapper__b.get_result()


class _NamesConverter:
    __doc__ = 'Convert name of a node to representation accepted by dot format.'
    _NamesConverter__pattern = re.compile('([\\"])')

    @staticmethod
    def run(name):
        escaped_name = re.sub(_NamesConverter._NamesConverter__pattern, '\\\\\\1', name)
        return escaped_name


class _NodeInfo:
    __doc__ = 'Information about the node stored by _NodesRegister'

    def __init__(self, has_visible_input_ports, has_visible_output_ports):
        self.has_visible_input_ports = has_visible_input_ports
        self.has_visible_output_ports = has_visible_output_ports


class _NodesRegister:
    __doc__ = 'Register of all nodes with information relevant to visualization.'

    def __init__(self):
        self._NodesRegister__nodes = {}

    def contains(self, node_name):
        """Args:
            node_name (string): name of the node
        """
        return node_name in self._NodesRegister__nodes

    def add(self, node_name, node_info):
        """Args:
            node_name (string): name of the node
            node_info (_NodeInfo):
        """
        if node_name in self._NodesRegister__nodes:
            raise Exception('Node with name {} already exists in the register.'.format(node_name))
        self._NodesRegister__nodes[node_name] = node_info

    def get(self, node_name):
        """Args:
            node_name (string): name of the node
        """
        return self._NodesRegister__nodes[node_name]


class _EdgesRegister:
    __doc__ = 'Register of all edges.'

    def __init__(self):
        self._EdgesRegister__starts = {}

    def contains(self, start, end):
        """Args:
            start (string): start of the edge
            end (string): end of the edge
        """
        if start not in self._EdgesRegister__starts:
            return False
        if end not in self._EdgesRegister__starts[start]:
            return False
        return True

    def add(self, start, end):
        """Args:
            start (string): start of the edge
            end (string): end of the edge
        """
        if start not in self._EdgesRegister__starts:
            self._EdgesRegister__starts[start] = set()
        if end in self._EdgesRegister__starts[start]:
            raise Exception('End "{}" already registered.'.format(end))
        self._EdgesRegister__starts[start].add(end)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/pipeline/pipeline.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 4769 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
import yaml
from enum import Enum, unique
import vipe.common.serialization
from vipe.common.utils import default_eq

@unique
class NodeImportance(Enum):
    __doc__ = 'Importance of the node in the data processing workflow.\n\n    The higher importance of the node, the more prominently it should be\n    shown on the graph. With the default details level of showing nodes\n    on the graph, the node with the `lowest` priority should be removed\n    from the graph.'
    lowest = 1
    very_low = 2
    low = 3
    normal = 4


class Pipeline(yaml.YAMLObject):
    __doc__ = 'A graph structure corresponding to workflow pipeline.\n\n    Producer-consumer dependencies are presented explicitly here. However,\n    the information about sequence of execution of consecutive workflow nodes\n    is gone.\n    '
    yaml_tag = '!Pipeline'

    def __init__(self, nodes):
        """
        Args:
            nodes (Dict[string, Node]): a dictionary mapping node of a node
                to a Node object.
        """
        self.nodes = nodes

    @staticmethod
    def get_input_node_name():
        """Name of a special node that defines data ingested by the pipeline.

        The node with this name might not be present in the pipeline."""
        return 'INPUT'

    @staticmethod
    def get_output_node_name():
        """Name of a special node that defines data produced by the pipeline.

        The node with this name might not be present in the pipeline."""
        return 'OUTPUT'

    def __eq__(self, other):
        return default_eq(self, other)

    def __str__(self):
        return self.to_yaml_dump()

    def to_yaml_dump(self):
        """Dump the graph to YAML.
        """
        return vipe.common.serialization.to_yaml(self)

    @staticmethod
    def from_yaml_dump(yaml_string):
        """Read the graph from YAML dump."""
        return vipe.common.serialization.from_yaml(yaml_string)


class Node(yaml.YAMLObject):
    yaml_tag = '!Node'

    def __init__(self, type_, input_ports, output_ports, importance=NodeImportance.normal):
        """
        Args:
            type_ (string): a description of the type of the node.
            input_ports (Dict[string, string]): ports from which the node takes
                data to consume.
                The key in the dictionary is the node of the port, the value
                is a data identifier. This is an identifier of the data
                consumed on this port. A producer port of one node is connected
                to a consumer port of another node by specifying the same
                data identifier.
            output_ports (Dict[string, string]): ports to which the node
                produces data. The meaning of the elements of the dictionary
                is analogous to `input_ports`.
            importance (Importance): how important given node is. This
                influences the presentation of the node on the graph.
        """
        self.type = type_
        self.input_ports = input_ports
        self.output_ports = output_ports
        self.importance = importance

    def __getstate__(self):
        """__getstate__() and __setstate__() methods are overriden.

        This is because enum field `self.importance` by default is not
        serialized to YAML nicely, namely the field is serialized as, e.g.:
             importance: &id001 !!python/object/apply:vipe.pipeline.pipeline.Importance
             - 4
        Overriding these two methods gives us control over how this
        enum field (and other fields as well) are serialized.
        """
        return {'type': self.type,  'input_ports': self.input_ports, 
         'output_ports': self.output_ports, 
         'importance': self.importance.name}

    def __setstate__(self, state):
        """See the comment to __getstate__() method"""
        self.type = state['type']
        self.input_ports = state['input_ports']
        self.output_ports = state['output_ports']
        self.importance = NodeImportance[state['importance']]

    def __eq__(self, other):
        return default_eq(self, other)
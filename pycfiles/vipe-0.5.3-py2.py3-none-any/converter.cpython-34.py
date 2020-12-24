# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/mafju/current/icm/iis_cr/vipe/vipe/oozie/converter/converter.py
# Compiled at: 2016-02-15 13:44:30
# Size of source mod 2**32: 3076 bytes
__author__ = 'Mateusz Kobos mkobos@icm.edu.pl'
from vipe.pipeline.pipeline import Pipeline

class PipelineConverter:
    __doc__ = 'Interface to be implemented by all classes that implement conversion of\n        OozieGraph to Pipeline.\n    '

    def convert_parameters(self, parameters):
        """Convert parameters defined in the header of a workflow to nodes.

        Args:
            parameters (Dict[string, string]): the key
                is the node of parameter and the value is it's value.

        Return:
            (vipe.pipeline.pipeline.Node, vipe.pipeline.pipeline.Node):
                the first element is the INPUT node that defines data ingested
                by the workflow and the second one is the OUTPUT node that
                defines data produced by the workflow. Either of them can be
                None.
        """
        return (None, None)

    def convert_node(self, name, oozie_node):
        """Convert OozieGraph's Node

        Args:
            name (string): name of the node
            oozie_node (vipe.oozie.graph.Node): OozieGraph's Node

        Returns:
            vipe.pipeline.pipeline.Node: Pipeline's Node. If `None` is
                returned, it is assumed that given node should be ignored.
        """
        raise NotImplementedError


def convert(oozie_graph, pipeline_converter):
    """Convert OozieGraph to Pipeline using given Converter

    Args:
        oozie_graph (OozieGraph):
        pipeline_converter (PipelineConverter):

    Returns:
        Pipeline
    """
    pipeline_nodes = {}
    input_node, output_node = pipeline_converter.convert_parameters(oozie_graph.parameters)
    for name, node in [(Pipeline.get_input_node_name(), input_node),
     (
      Pipeline.get_output_node_name(), output_node)]:
        if node is not None:
            pipeline_nodes[name] = node
            continue

    for name, oozie_node in oozie_graph.nodes.items():
        reserved_names = [
         Pipeline.get_input_node_name(),
         Pipeline.get_output_node_name()]
        if name in reserved_names:
            raise Exception('Name of one of Oozie nodes ({}) is one of the reserved names: {}.'.format(name, ', '.join(reserved_names)))
        pipeline_node = pipeline_converter.convert_node(name, oozie_node)
        if pipeline_node is not None:
            pipeline_nodes[name] = pipeline_node
            continue

    return Pipeline(pipeline_nodes)
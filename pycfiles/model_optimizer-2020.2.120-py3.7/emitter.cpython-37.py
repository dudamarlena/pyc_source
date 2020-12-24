# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/back/ie_ir_ver_2/emitter.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 19335 bytes
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
import hashlib
from defusedxml.minidom import parseString
from xml.etree.ElementTree import Element, SubElement, tostring
from mo.graph.graph import *
from mo.middle.passes.convert_data_type import data_type_str_to_precision, np_data_type_to_precision
from mo.utils.unsupported_ops import UnsupportedOps
from mo.utils.utils import refer_to_faq_msg
from mo.utils.version import get_version

def serialize_constants(graph: Graph, bin_file_name: str, data_type=np.float32):
    """
    Found all data constants that has output edges with 'bin' attribute.
    Serialize content for such constants to a binary file with name bin_file_name in
    raw format. Save offset and length of serialized area in the file as 'offset' and 'size'
    attributes of data node.

    Args:
        @graph: input graph with op and data nodes
        @bin_file_name: path to file to write blobs to
        @data_type: numpy data type to convert all blob elemnts to

    """
    bin_hashes = {}
    with open(bin_file_name, 'wb') as (bin_file):
        serialize_constants_recursively(graph, bin_file, data_type, bin_hashes)


def update_offset_size_in_const_node(node: Node):
    assert node.kind == 'data'
    for consumer in node.out_nodes():
        if consumer.type != 'Const':
            continue
        assert not consumer.has_valid('offset')
        assert not consumer.has_valid('size')
        consumer['offset'] = node.offset
        consumer['size'] = node.size


def serialize_constants_recursively(graph: Graph, bin_file, data_type, bin_hashes):
    nodes = sorted(graph.nodes())
    for node in nodes:
        node = Node(graph, node)
        if node.kind == 'data' and node.value is not None:
            if any(('bin' in d for u, v, d in graph.out_edges((node.node), data=True))):
                blob = node.value
                blob_hash = hashlib.sha512(blob.tobytes()).hexdigest()
                if blob_hash in bin_hashes and np.array_equal(blob, bin_hashes[blob_hash]['blob']):
                    graph.node[node.node]['offset'] = bin_hashes[blob_hash]['offset']
                    graph.node[node.node]['size'] = bin_hashes[blob_hash]['size']
                    graph.node[node.node]['blob_precision'] = np_data_type_to_precision(blob.dtype)
                    if graph.graph['cmd_params'].generate_experimental_IR_V10:
                        update_offset_size_in_const_node(node)
                else:
                    start = bin_file.tell()
                    blob.tofile(bin_file)
                end = bin_file.tell()
                graph.node[node.node]['offset'] = start
                graph.node[node.node]['size'] = end - start
                graph.node[node.node]['blob_precision'] = np_data_type_to_precision(blob.dtype)
                bin_hashes[blob_hash] = {'offset':graph.node[node.node]['offset'], 
                 'size':graph.node[node.node]['size'], 
                 'blob':blob}
                if graph.graph['cmd_params'].generate_experimental_IR_V10:
                    update_offset_size_in_const_node(node)
            if not blob.dtype.itemsize * np.prod(node.shape) == end - start:
                assert node.has_valid('force_shape'), node.attrs()
            log.debug("Detected binary for graph: '{}', node: '{}', id: {}, shape: '{}', offset: '{}', size: '{}'".format(graph, node.soft_get('name'), node.id, node.shape, node.offset, node.size))

    for node in nodes:
        node = Node(graph, node)
        if node.has_valid('sub_graphs'):
            for sub_graph_attr_name in node.sub_graphs:
                sub_graph = node[sub_graph_attr_name]
                serialize_constants_recursively(sub_graph, bin_file, data_type, bin_hashes)


def serialize_mean_image(bin_file_name: str, mean_data=[]):
    with open(bin_file_name, 'ab') as (bin_file):
        mean_offset = []
        mean_size = []
        for x in range(len(mean_data)):
            start = bin_file.tell()
            bin_file.write(mean_data[x][:])
            end = bin_file.tell()
            mean_offset.append(start)
            mean_size.append(end - start)

        return (mean_offset, mean_size)


def xml_shape(shape: np.ndarray, element: Element):
    for d in shape:
        dim = SubElement(element, 'dim')
        if d < 0:
            raise Error('The value "{}" for shape is less 0. May be the input shape of the topology is wrong.'.format(d))
        if int(d) != d:
            raise Error('The value "{}" for shape is not integer.'.format(d))
        if not isinstance(d, np.int64):
            log.warning('The element of shape is not np.int64 value. Converting the value "{}" to integer'.format(d))
            d = int(d)
        dim.text = str(d)


def xml_ports(node: Node, element: Element, edges: Element):
    inputs = None
    for u, d in node.get_sorted_inputs():
        if 'bin' not in d:
            if not 'xml_skip' not in d:
                if d['xml_skip'] or inputs is None:
                    inputs = SubElement(element, 'input')
                port = SubElement(inputs, 'port')
                port.set('id', str(d['in']))
                assert node.graph.node[u]['shape'] is not None, 'Input shape is not calculated properly for node {}'.format(node.id)
                xml_shape(node.graph.node[u]['shape'], port)
                assert node.graph.node[u]['kind'] == 'data'
                in_nodes = list(node.graph.in_edges(u, data=True))
                if not len(in_nodes) <= 1:
                    raise AssertionError
            if len(in_nodes) == 1:
                src, _, out_attrs = in_nodes[0]
                edge = SubElement(edges, 'edge')
                edge.set('from-layer', str(src))
                edge.set('from-port', str(out_attrs['out']))
                edge.set('to-layer', str(node.node))
                edge.set('to-port', str(d['in']))

    outputs = None
    for v, d in node.get_sorted_outputs():
        if not 'xml_skip' not in d:
            if d['xml_skip'] or outputs is None:
                outputs = SubElement(element, 'output')
            port = SubElement(outputs, 'port')
            port.set('id', str(d['out']))
            port_id = d['out'] - len(node.in_nodes())
            data_type = node.out_port(port_id).get_data_type()
            assert data_type is not None, 'The precision is not defined for the output port {} of node {}'.format(port_id, node.soft_get('name'))
            port.set('precision', node.soft_get('force_type', np_data_type_to_precision(data_type)))
            assert node.graph.node[v]['shape'] is not None, 'Output shape is not calculated properly for node {}'.format(node.id)
            xml_shape(node.graph.node[v]['shape'], port)


def xml_consts(graph: Graph, node: Node, element: Element):
    blobs = None
    for u, d in node.get_sorted_inputs():
        if 'bin' in d:
            if not node.type != 'Const':
                if not (graph.graph['cmd_params'].generate_experimental_IR_V10 or blobs):
                    blobs = SubElement(element, 'blobs')
            const = SubElement(blobs, d['bin'])
            try:
                const.set('offset', str(graph.node[u]['offset']))
                const.set('size', str(graph.node[u]['size']))
                const.set('precision', graph.node[u]['blob_precision'])
            except Exception as e:
                try:
                    raise Error('Unable to access binary attributes ("offset" and/or "size") for blobs for node {}. Details: {}'.format(node.soft_get('name'), e))
                finally:
                    e = None
                    del e


def soft_get(node, attr):
    """ If node has soft_get callable member, returns node.soft_get(attr), else return <SUB-ELEMENT> """
    if hasattr(node, 'soft_get'):
        if callable(node.soft_get):
            return node.soft_get(attr)
    return '<SUB-ELEMENT>'


def serialize_element(graph: Graph, node, schema: list, parent_element: Element, edges: Element, unsupported):
    name, attrs, subelements = schema
    element = SubElement(parent_element, name)
    for attr in attrs:
        if isinstance(attr, tuple):
            key = attr[0]
            try:
                if callable(attr[1]):
                    value = attr[1](node)
                else:
                    value = node[attr[1]] if attr[1] in node else None
            except TypeError as e:
                try:
                    raise Error('Unable to extract {} from layer {}', key, soft_get(node, 'name')) from e
                finally:
                    e = None
                    del e

            except Exception as e:
                try:
                    raise Error('Cannot emit value for attribute {} for layer {}. Internal attribute template: {}.', key, soft_get(node, 'name'), attr) from e
                finally:
                    e = None
                    del e

        else:
            if isinstance(attr, dict):
                node_attrs = node.graph.node[node.id] if isinstance(node, Node) else node
                for key in attr.keys():
                    if key in node_attrs:
                        for k, v in node_attrs[key].items():
                            element.set(k, str(v))

                continue
            else:
                key = attr
                value = node[attr] if attr in node else None
        if value is not None:
            element.set(key, str(value))

    serialize_node_attributes(graph, node, subelements, element, edges, unsupported)
    if len(element.attrib) == 0:
        if len(element.getchildren()) == 0:
            parent_element.remove(element)


def serialize_meta_list(graph, node, schema, element, edges, unsupported):
    _, list_accessor, sub_schema = schema
    items = list_accessor(node)
    for item in items:
        serialize_node_attributes(graph, item, [sub_schema], element, edges, unsupported)


def serialize_node_attributes(graph: Graph, node, schema: list, parent_element: Element, edges: Element, unsupported):
    if isinstance(node, Node):
        if node.soft_get('result' == 'Result'):
            if node.has_and_set('remove_from_xml'):
                return
    try:
        for s in schema:
            if not isinstance(s, tuple):
                if s == '@ports':
                    try:
                        xml_ports(node, parent_element, edges)
                    except Exception as e:
                        try:
                            raise Error(('Unable to create ports for node with id {}. ' + refer_to_faq_msg(3)).format(node.id)) from e
                        finally:
                            e = None
                            del e

                else:
                    if s == '@consts':
                        xml_consts(graph, node, parent_element)
                    else:
                        log.warning('Unknown xml schema tag: {}'.format(s))
            else:
                name = s[0]
                if name == '@list':
                    serialize_meta_list(graph, node, s, parent_element, edges, unsupported)
                elif name == '@network':
                    serialize_network(node[s[1]], parent_element, unsupported)
                else:
                    serialize_element(graph, node, s, parent_element, edges, unsupported)

    except Exception as e:
        try:
            raise Error('Error while emitting attributes for layer {} (id = {}). It usually means that there is unsupported pattern around this node or unsupported combination of attributes.', soft_get(node, 'name'), node.id) from e
        finally:
            e = None
            del e


def create_pre_process_block_for_image(net: Element, ref_layer_names: list, mean_offset: tuple, mean_size: tuple):
    pre_process = SubElement(net, 'pre-process')
    pre_process.set('mean-precision', 'FP32')
    pre_process.set('reference-layer-name', ref_layer_names[0])
    for idx in range(len(mean_size)):
        channel_xml = SubElement(pre_process, 'channel')
        channel_xml.set('id', str(idx))
        mean_xml = SubElement(channel_xml, 'mean')
        mean_xml.set('offset', str(mean_offset[idx]))
        mean_xml.set('size', str(mean_size[idx]))


def create_pre_process_block(net, ref_layer_name, means, scales=None):
    """
    Generates the pre-process block for the IR XML
    Args:
        net: root XML element
        ref_layer_name: name of the layer where it is referenced to
        means: tuple of values
        scales: tuple of values

    Returns:
        pre-process XML element
    """
    pre_process = SubElement(net, 'pre-process')
    pre_process.set('reference-layer-name', ref_layer_name)
    for idx in range(len(means)):
        channel_xml = SubElement(pre_process, 'channel')
        channel_xml.set('id', str(idx))
        mean_xml = SubElement(channel_xml, 'mean')
        mean_xml.set('value', str(means[idx]))
        if scales:
            scale_xml = SubElement(channel_xml, 'scale')
            scale_xml.set('value', str(scales[idx]))

    return pre_process


def add_quantization_statistics(graph, net_element):
    if 'statistics' in graph.graph:
        stats = SubElement(net_element, 'statistics')
        for tensor, interval in graph.graph['statistics'].items():
            layer = SubElement(stats, 'layer')
            name = SubElement(layer, 'name')
            name.text = tensor
            min = SubElement(layer, 'min')
            min.text = interval['min']
            max = SubElement(layer, 'max')
            max.text = interval['max']

        log.info('Statistics were inserted to IR')


def add_quantization_info_section(net: Element, meta_info: dict):
    if 'quantization_parameters' in meta_info:
        parameters = meta_info['quantization_parameters']
        quant_params = SubElement(net, 'quantization_parameters')
        config = SubElement(quant_params, 'config')
        config.text = parameters['config']
        version = SubElement(quant_params, 'version')
        version.set('value', parameters['version'])
        cli_params = SubElement(quant_params, 'cli_params')
        cli_params.set('value', parameters['cli_params'])


def add_meta_data(net: Element, meta_info: dict):
    meta = SubElement(net, 'meta_data')
    SubElement(meta, 'MO_version').set('value', get_version())
    parameters = SubElement(meta, 'cli_parameters')
    [SubElement(parameters, str(key)).set('value', str(meta_info[key])) for key in sorted(meta_info.keys()) if key not in ('unset',
                                                                                                                           'quantization_parameters')]
    SubElement(parameters, 'unset').set('unset_cli_parameters', ', '.join(sorted(meta_info['unset'])))


def serialize_network(graph, net_element, unsupported):
    layers = SubElement(net_element, 'layers')
    edges = SubElement(net_element, 'edges')
    if graph is None:
        return
    nodes = sorted(graph.nodes())
    for node in nodes:
        node = Node(graph, node)
        if node.kind == 'op':
            if not node.has('type') or node.type is None:
                unsupported.add(node)
                continue
        if not node.has('IE'):
            continue
        try:
            serialize_node_attributes(graph, node, node.IE, layers, edges, unsupported)
        except Error as e:
            try:
                raise Error(str(e).replace('<SUB-ELEMENT>', '{} (id = {})'.format(node.soft_get('name'), node.id))) from e
            finally:
                e = None
                del e


def generate_ie_ir(graph: Graph, file_name: str, input_names: tuple=(), mean_offset: tuple=(), mean_size: tuple=(), meta_info: dict=dict()):
    """
    Extracts IE/IR attributes from kind='op' nodes in three ways:
      (1) node.IE xml scheme that set correspondance from existing attributes to generated xml elements
      (2) input/output edges that don't have 'bin' attributes are transformed to input/output ports
      (3) input edges that has 'bin' attributes are handled in special way like weights/biases

    Args:
        graph: nx graph with FW-independent model
        file_name: name of the resulting IR
        input_names: names of input layers of the topology to add mean file to
        input_name: name of the layer which is referenced from pre-processing block if any
        mean_values: tuple of mean values for channels in RGB order
        scale_values:  tuple of mean values for channels in RGB order
        mean_offset: offset in binary file, where mean file values start
        mean_size: size of the mean file
    """
    net = Element('net')
    net.set('name', graph.name)
    net.set('version', str(graph.graph['ir_version']))
    if mean_size or mean_offset:
        create_pre_process_block_for_image(net, input_names, mean_offset, mean_size)
    if 'mean_values' in graph.graph.keys():
        for input_name, values in graph.graph['mean_values'].items():
            create_pre_process_block(net, input_name, values)

    unsupported = UnsupportedOps(graph)
    serialize_network(graph, net, unsupported)
    add_quantization_statistics(graph, net)
    add_meta_data(net, meta_info)
    add_quantization_info_section(net, meta_info)
    xml_string = tostring(net)
    xml_doc = parseString(xml_string)
    pretty_xml_as_string = xml_doc.toprettyxml()
    if len(unsupported.unsupported):
        log.debug('Partially correct IR XML:\n{}'.format(pretty_xml_as_string))
        unsupported.report(log.error, 'List of operations that cannot be converted to Inference Engine IR:')
        raise Error('Part of the nodes was not converted to IR. Stopped. ' + refer_to_faq_msg(24))
    with open(file_name, 'wb') as (file):
        file.write(bytes(pretty_xml_as_string, 'UTF-8'))


def port_renumber(graph: Graph):
    for node in list(graph.nodes()):
        node = Node(graph, node)
        if node.kind == 'op':
            base = 0
            for u, d in node.get_sorted_inputs():
                d['in'] = base
                base += 1

            for v, d in node.get_sorted_outputs():
                d['out'] = base
                base += 1
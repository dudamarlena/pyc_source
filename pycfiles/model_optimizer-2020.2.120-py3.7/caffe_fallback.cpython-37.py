# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mo/front/common/partial_infer/caffe_fallback.py
# Compiled at: 2020-05-01 08:37:21
# Size of source mod 2**32: 4349 bytes
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
import logging as log, os, networkx as nx, numpy as np
from mo.graph.graph import Node, Graph
from mo.utils.error import Error
import mo.utils.find_inputs as find_inputs
from mo.utils.utils import refer_to_faq_msg

def get_node_top(graph: Graph, name: str):
    node = Node(graph, name)
    if node:
        return node.out_edge()['name']


def build_net(graph: Graph):
    try:
        if not hasattr(os.environ, 'GLOG_minloglevel'):
            os.environ['GLOG_minloglevel'] = '2'
        import caffe
        log.info('Partial inference via the framework is available')
    except ImportError:
        log.warning('pyCaffe is not available. Partial inference via the framework is not possible')
        return
    else:
        try:
            net = caffe.Net(graph.proto_path, graph.caffemodel_path, caffe.TEST)
        except Exception as err:
            try:
                raise Error('Error happened while constructing caffe.Net in the Caffe fallback function: {}. ' + refer_to_faq_msg(12), str(err)) from err
            finally:
                err = None
                del err

        inputs_node_name = find_inputs(graph)
        reshape_flag = False
        for i in inputs_node_name:
            new_input_shape = graph.node[i]['shape'].astype(int)
            top_node = get_node_top(graph, i)
            caffe_shape = list(net.blobs[top_node].shape)
            if not np.all(caffe_shape == new_input_shape):
                (net.blobs[top_node].reshape)(*[int(x) for x in new_input_shape])
                reshape_flag = True

        if reshape_flag:
            net.reshape()
        try:
            net.forward()
        except KeyError as err:
            try:
                log.error('Error happened in Caffe net.forward: {}.'.format(str(err)))
                log.error('It may point to the known bug in pycaffe when top and name of the layer do not match.')
                log.error('Please make sure that the latest pycaffe is used.')
                raise Error('Cannot infer shapes due to exception in Caffe: {}. ' + refer_to_faq_msg(13), str(err)) from err
            finally:
                err = None
                del err

        except Exception as err:
            try:
                raise Error('Cannot infer shapes in Caffe net.forward due to exception: {}.' + refer_to_faq_msg(13), str(err)) from err
            finally:
                err = None
                del err

        graph.__setattr__('caffe_net', net)


def get_net(graph: Graph):
    if not graph:
        return
    if graph:
        if not hasattr(graph, 'caffe_net'):
            build_net(graph)
    return getattr(graph, 'caffe_net', None)


def caffe_native_node_infer(node: Node):
    """
    Infers shape of the unknown operation via Caffe if it is available.
    Requires graph to contain paths to both prototxt and caffemodel files.
    When it is visited for the first time, net object is created and written to graph.
    Next time, it just takes the built net from graph.

    Parameters
    ----------
    node node to infer the shape for

    """
    log.error('Caffe fallback is deprecated. It will be removed in future releases. Please use extensions for unsupported layers.\nSee more information in the "Custom Layers in the Model Optimizer" chapter of the Model Optimizer Developer Guide', extra={'is_warning': True})
    log.info('Called "caffe_native_node_infer" for node "{}"'.format(node.id))
    graph = node.graph
    net = get_net(graph)
    if not net:
        raise Error('Cannot infer shape for node "{}" because there is no Caffe available. Please register python infer function for op = {} or use Caffe for shape inference. ' + refer_to_faq_msg(14), node.soft_get('name'), node.soft_get('op'))
    for iout in range(len(node.out_nodes())):
        output_shape = np.array((net.blobs[node.top].data.shape), dtype=(np.int64))
        node.out_node(iout).shape = output_shape
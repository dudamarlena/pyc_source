# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/extensions/back/blob_normalizer.py
# Compiled at: 2020-05-01 08:37:19
# Size of source mod 2**32: 2797 bytes
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
from extensions.back.op_versioning import OpVersioning
from mo.back.replacement import BackReplacementPattern
from mo.graph.graph import Graph

class BlobNormalizer(BackReplacementPattern):
    __doc__ = '\n    This pass affects Convolution and FullyConnected weights and biases form in IR.\n    Old version of those layers included weights and biases as blobs:\n    <layer ... type="Convolution">\n        ...\n        <blobs>\n            <weights offset="***" size="***"/>\n            <biases offset="***" size="***"/>\n        </blobs>\n    </layer>\n\n    New version (after BlobNormalizer execution) weighs and biases are represented\n    as inputs to Convolution/FullyConnected layer\n    '
    enabled = True
    graph_condition = [
     lambda graph: graph.graph['cmd_params'].blobs_as_inputs or graph.graph['cmd_params'].generate_experimental_IR_V10]

    def run_before(self):
        return []

    def run_after(self):
        from extensions.back.pass_separator import BackFinish
        return [
         BackFinish]

    @staticmethod
    def pattern():
        return dict(nodes=[
         (
          'conv', dict(type=(lambda type: type in ('Convolution', 'Deconvolution', 'FullyConnected'))))],
          edges=[])

    def replace_pattern(self, graph: Graph, match: dict):
        conv = match['conv']
        for i in (1, 2):
            if i in conv.in_edges() and conv.in_edges()[i] and 'bin' in conv.in_edges()[i]:
                del conv.in_edges()[i]['bin']

    def find_and_replace_pattern--- This code section failed: ---

 L.  64         0  LOAD_FAST                'graph'
                2  LOAD_ATTR                graph
                4  LOAD_STR                 'cmd_params'
                6  BINARY_SUBSCR    
                8  LOAD_ATTR                generate_experimental_IR_V10
               10  POP_JUMP_IF_FALSE   144  'to 144'

 L.  65        12  SETUP_LOOP           92  'to 92'
               14  LOAD_FAST                'graph'
               16  LOAD_METHOD              get_op_nodes
               18  CALL_METHOD_0         0  '0 positional arguments'
               20  GET_ITER         
               22  FOR_ITER             90  'to 90'
               24  STORE_FAST               'node'

 L.  66        26  LOAD_FAST                'node'
               28  LOAD_METHOD              soft_get
               30  LOAD_STR                 'type'
               32  CALL_METHOD_1         1  '1 positional argument'
               34  LOAD_METHOD              lower
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  LOAD_GLOBAL              OpVersioning
               40  LOAD_ATTR                opset_1_types
               42  COMPARE_OP               not-in
               44  POP_JUMP_IF_FALSE    48  'to 48'

 L.  67        46  CONTINUE             22  'to 22'
             48_0  COME_FROM            44  '44'

 L.  68        48  SETUP_LOOP           88  'to 88'
               50  LOAD_FAST                'node'
               52  LOAD_METHOD              in_edges
               54  CALL_METHOD_0         0  '0 positional arguments'
               56  LOAD_METHOD              items
               58  CALL_METHOD_0         0  '0 positional arguments'
               60  GET_ITER         
             62_0  COME_FROM            76  '76'
               62  FOR_ITER             86  'to 86'
               64  UNPACK_SEQUENCE_2     2 
               66  STORE_FAST               '_'
               68  STORE_FAST               'd'

 L.  69        70  LOAD_STR                 'bin'
               72  LOAD_FAST                'd'
               74  COMPARE_OP               in
               76  POP_JUMP_IF_FALSE    62  'to 62'

 L.  70        78  LOAD_FAST                'd'
               80  LOAD_STR                 'bin'
               82  DELETE_SUBSCR    
               84  JUMP_BACK            62  'to 62'
               86  POP_BLOCK        
             88_0  COME_FROM_LOOP       48  '48'
               88  JUMP_BACK            22  'to 22'
               90  POP_BLOCK        
             92_0  COME_FROM_LOOP       12  '12'

 L.  71        92  SETUP_LOOP          172  'to 172'
               94  LOAD_FAST                'graph'
               96  LOAD_METHOD              get_data_nodes
               98  CALL_METHOD_0         0  '0 positional arguments'
              100  GET_ITER         
              102  FOR_ITER            140  'to 140'
              104  STORE_FAST               'node'

 L.  72       106  SETUP_LOOP          138  'to 138'
              108  LOAD_FAST                'node'
              110  LOAD_METHOD              in_edges
              112  CALL_METHOD_0         0  '0 positional arguments'
              114  GET_ITER         
            116_0  COME_FROM           126  '126'
              116  FOR_ITER            136  'to 136'
              118  STORE_FAST               'd'

 L.  73       120  LOAD_STR                 'bin'
              122  LOAD_FAST                'd'
              124  COMPARE_OP               in
              126  POP_JUMP_IF_FALSE   116  'to 116'

 L.  74       128  LOAD_FAST                'd'
              130  LOAD_STR                 'bin'
              132  DELETE_SUBSCR    
              134  JUMP_BACK           116  'to 116'
              136  POP_BLOCK        
            138_0  COME_FROM_LOOP      106  '106'
              138  JUMP_BACK           102  'to 102'
              140  POP_BLOCK        
              142  JUMP_FORWARD        172  'to 172'
            144_0  COME_FROM            10  '10'

 L.  76       144  LOAD_GLOBAL              len
              146  LOAD_FAST                'graph'
              148  LOAD_ATTR                get_op_nodes
              150  LOAD_STR                 'FakeQuantize'
              152  LOAD_CONST               ('type',)
              154  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              156  CALL_FUNCTION_1       1  '1 positional argument'
              158  POP_JUMP_IF_FALSE   172  'to 172'

 L.  77       160  LOAD_GLOBAL              BackReplacementPattern
              162  LOAD_METHOD              find_and_replace_pattern
              164  LOAD_FAST                'self'
              166  LOAD_FAST                'graph'
              168  CALL_METHOD_2         2  '2 positional arguments'
              170  POP_TOP          
            172_0  COME_FROM           158  '158'
            172_1  COME_FROM           142  '142'
            172_2  COME_FROM_LOOP       92  '92'

Parse error at or near `COME_FROM' instruction at offset 172_1
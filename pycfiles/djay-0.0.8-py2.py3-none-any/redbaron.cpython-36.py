# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-x0nyl_ya/redbaron/redbaron/redbaron.py
# Compiled at: 2019-07-30 18:47:05
# Size of source mod 2**32: 2683 bytes
from __future__ import absolute_import
import baron, baron.path
from baron.utils import string_instance
from redbaron import nodes, base_nodes

class RedBaron(base_nodes.GenericNodesUtils, base_nodes.LineProxyList):

    def __init__(self, source_code):
        self.first_blank_lines = []
        if isinstance(source_code, string_instance):
            self.node_list = base_nodes.NodeList.from_fst((baron.parse(source_code)), parent=self, on_attribute='root')
            self.middle_separator = nodes.DotNode({'type':'endl',  'formatting':[],  'value':'\n',  'indent':''})
            self.data = []
            previous = None
            for i in self.node_list:
                if i.type != 'endl':
                    self.data.append([i, []])
                else:
                    if previous:
                        if previous.type == 'endl':
                            self.data.append([previous, []])
                if previous is None:
                    if i.type == 'endl':
                        self.data.append([i, []])
                if self.data:
                    self.data[(-1)][1].append(i)
                previous = i

            self.node_list.parent = None
        else:
            super(RedBaron, self).__init__(source_code)
        self.on_attribute = None
        self.parent = None

    def _convert_input_to_node_object(self, value, parent, on_attribute):
        return base_nodes.GenericNodesUtils._convert_input_to_node_object(self, value, self, 'root')

    def _convert_input_to_node_object_list(self, value, parent, on_attribute):
        return base_nodes.GenericNodesUtils._convert_input_to_node_object_list(self, value, self, 'root')
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/datalogue/models/transformations/add.py
# Compiled at: 2020-05-12 19:42:15
# Size of source mod 2**32: 3524 bytes
from typing import List, Union
from datalogue.errors import DtlError, _property_not_found, _invalid_property_type
from datetime import datetime
from datalogue.models.transformations.commons import Transformation, DataType
from datalogue.dtl_utils import _parse_list

class NodeDescription:
    __doc__ = '\n    Description of a node to be added to the tree.\n    '

    def __init__(self, path: List[str], value: Union[(str, bool, int, float, datetime)], value_type: DataType):
        """
        :param path: path of the node to be created
        :param value: value to be set for the node
        :param value_type: type of the value to be used
        """
        self.path = path
        self.value = value
        self.value_type = value_type

    def __eq__(self, other: 'NodeDescription'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"NodeDescription(path: {'.'.join(self.path)}, value: {self.value!r}, type: {self.value_type!r})"

    def _as_payload(self) -> Union[(DtlError, dict)]:
        value = self.value
        if isinstance(value, datetime):
            value = value.isoformat()
        else:
            value = str(value)
        return {'path':self.path, 
         'value':value, 
         'valueType':self.value_type.value}

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'NodeDescription')]:
        path = json.get('path')
        if path is None:
            return _property_not_found('path', json)
        if not isinstance(path, list):
            return _invalid_property_type('path', 'List[str]', json)
        value = json.get('value')
        if value is None:
            return _property_not_found('value', json)
        if not isinstance(value, str):
            return _invalid_property_type('value', 'str', json)
        value_type = json.get('valueType')
        if value_type is None:
            return _property_not_found('valueType', json)
        else:
            value_type = DataType.from_str(value_type)
            if isinstance(value_type, DtlError):
                return value_type
            return NodeDescription(path, value, value_type)


class Add(Transformation):
    __doc__ = "\n    Adds a node to the graph\n\n    Some edge cases:\n        - If the specified path's parent do not exists, the node will not be created\n        - If the cast cannot happen for the given value, the node will node be created\n    "
    type_str = 'Add'

    def __init__(self, nodes: List[NodeDescription]):
        """
        :param nodes: List of nodes to be added to the tree
        """
        Transformation.__init__(self, Add.type_str)
        self.nodes = nodes

    def __eq__(self, other: 'Add'):
        if isinstance(self, other.__class__):
            return self._as_payload() == other._as_payload()
        else:
            return False

    def __repr__(self):
        return f"Add(nodes: {self.nodes})"

    def _as_payload(self) -> dict:
        base = self._base_payload()
        base['nodes'] = list(map(lambda x: x._as_payload(), self.nodes))
        return base

    @staticmethod
    def _from_payload(json: dict) -> Union[(DtlError, 'Add')]:
        nodes = json.get('nodes')
        if nodes is None:
            return _property_not_found('nodes', json)
        else:
            nodes = _parse_list(NodeDescription._from_payload)(nodes)
            if isinstance(nodes, DtlError):
                return nodes
            return Add(nodes)
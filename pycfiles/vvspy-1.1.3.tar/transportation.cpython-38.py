# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: Y:\PyCharm\vvs\vvspy\obj\transportation.py
# Compiled at: 2019-12-07 13:33:32
# Size of source mod 2**32: 1607 bytes
from .line_operator import LineOperator

class Transportation:
    __doc__ = '\n\n        Describes info about transportation of a :class:`Connection`.\n\n        Attributes\n        -----------\n\n        raw :class:`dict`\n            Raw dict received by the API.\n        id :class:`str`\n            id of the transportation.\n        name :class:`str`\n            name of the transportation.\n        disassembled_name :class:`str`\n            detailed name of the transportation.\n        number :class:`str`\n            line number of the transportation.\n        description :class:`str`\n            description, most of the time the string that is displayed on the bus/train itself.\n        product :class:`dict`\n            describes the mean of transport (bus, train, etc.)\n        operator :class:`LineOperator`\n            describes the Operator of the transport.\n        destination :class:`dict`\n            destination of the transport.\n        properties :class:`dict`\n            misc info about the transport.\n    '

    def __init__(self, **kwargs):
        self.id = kwargs.get('id')
        self.name = kwargs.get('name')
        self.disassembled_name = kwargs.get('disassembledName', 'Walk')
        self.number = kwargs.get('number')
        self.description = kwargs.get('description')
        self.product = kwargs.get('product')
        self.operator = LineOperator(**kwargs.get('operator', {}))
        self.destination = kwargs.get('destination')
        self.raw = kwargs
        self.properties = kwargs.get('properties')
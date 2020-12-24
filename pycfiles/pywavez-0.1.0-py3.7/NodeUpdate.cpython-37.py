# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pywavez/NodeUpdate.py
# Compiled at: 2018-12-18 13:40:44
# Size of source mod 2**32: 2001 bytes


class NodeUpdate:
    __slots__ = ('id', )

    def __init__(self, id):
        self.id = id


class NodeUpdateTypes:

    class ProtocolInfo(NodeUpdate):
        __slots__ = ('protocolInfo', )

        def __init__(self, id, pi):
            super().__init__(id)
            self.protocolInfo = pi

        def __repr__(self):
            return f"<NodeUpdate.ProtocolInfo nodeId={self.id} protocolInfo={self.protocolInfo!r}>"

    class CommandClass(NodeUpdate):
        __slots__ = ('endpoint', 'class_', 'code', 'version')

        def __init__(self, id, endpoint, class_, code, version):
            super().__init__(id)
            self.endpoint = endpoint
            self.class_ = class_
            self.code = code
            self.version = version

        def __repr__(self):
            return f"<NodeUpdate.CommandClass nodeId={self.id} endpoint={self.endpoint} class_={self.class_!r} code={self.code} version={self.version}>"

    class ManufacturerInfo(NodeUpdate):
        __slots__ = ('manufacturerId', 'productTypeId', 'productId')

        def __init__(self, id, cmd):
            super().__init__(id)
            self.manufacturerId = cmd.manufacturerId
            self.productTypeId = cmd.productTypeId
            self.productId = cmd.productId

        def __repr__(self):
            return f"<NodeUpdate.ManufacturerInfo nodeId={self.id} manufacturerId=0x{self.manufacturerId:04x} productTypeId=0x{self.productTypeId:04x} productId=0x{self.productId:04x}>"


for key in dir(NodeUpdateTypes):
    if not key.startswith('_'):
        setattr(NodeUpdate, key, getattr(NodeUpdateTypes, key))
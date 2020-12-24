# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pywidl/interface.py
# Compiled at: 2012-03-21 11:41:42
from core import IPyWIdlObject

class IDefinition(IPyWIdlObject):
    name = None
    extended_attributes = []


class IInterface(IDefinition):
    parent = None
    members = []


class IInterfaceMember(IPyWIdlObject):
    name = None


class IAttribute(IInterfaceMember):
    inherit = False
    readonly = False
    type = None


class IType(IPyWIdlObject):
    name = None
    nullable = None


class ISingleType(IType):
    pass


class IPrimitiveType(ISingleType):
    pass


class IIntegerType(IPrimitiveType):
    pass


class IShort(IIntegerType):
    name = 'Short'


class IUnsignedShort(IIntegerType):
    name = 'UnsignedShort'


class ILong(IIntegerType):
    name = 'Long'


class IUnsignedLong(IIntegerType):
    name = 'UnsignedLong'


class ILongLong(IIntegerType):
    name = 'LongLong'


class IUnsignedLongLong(IIntegerType):
    name = 'UnsignedLongLong'


class IBoolean(IPrimitiveType):
    name = 'Boolean'


class IByte(IPrimitiveType):
    name = 'Byte'


class IOctet(IPrimitiveType):
    name = 'Octet'


class IFloat(IPrimitiveType):
    name = 'Float'


class IDouble(IPrimitiveType):
    name = 'Double'


class IDOMString(ISingleType):
    name = 'String'


class IInterfaceType(ISingleType):
    pass


class ISequence(ISingleType):
    name = 'Sequence'
    t = None


class IObject(ISingleType):
    name = 'Object'


class IDate(ISingleType):
    name = 'Date'


class IAny(ISingleType):
    name = 'Any'


class IArray(IType):
    name = 'Array'
    t = None


class IUnionType(IType):
    t = []
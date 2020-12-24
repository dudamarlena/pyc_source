# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/slow/model/sqldata_model.py
# Compiled at: 2006-01-10 04:15:14
from lxml.etree import SubElement, Element, ElementBase, Namespace
SQL_NAMESPACE_URI = 'http://www.dvs1.informatik.tu-darmstadt.de/research/OverML/sql'
MAX_NUMERIC_BITS = 256

class SqlDataType(ElementBase):
    __module__ = __name__

    def _is_typedef(self):
        return self.get('type_name', None) is not None

    def _is_typeref(self):
        return self.get('access_name', None) is not None

    @property
    def base_type(self):
        return self.tag.split('}', 1)[(-1)]

    @property
    def attributes(self):
        return tuple(self.ATTRIBUTES[self.base_type])

    def __getattr__(self, name):
        return self.attrib[name]

    def __setattr__(self, name, value):
        self.attrib[name] = value


class SimpleType(SqlDataType):
    __module__ = __name__

    def type_precision(self):
        return self.BIT_PRECISION[self.base_type]

    ATTRIBUTES = {'bytea': ['length'], 'boolean': (), 'smallint': ('minval', 'maxval'), 'integer': ('minval', 'maxval'), 'bigint': ('minval', 'maxval'), 'real': (), 'double': (), 'decimal': ['bits'], 'money': (), 'text': ('minlength', 'maxlength'), 'char': ['length'], 'interval': (), 'date': (), 'time': (), 'timestamp': (), 'timetz': ['timezone'], 'timestamptz': ['timezone'], 'inet': ('version', 'netmask'), 'macaddr': ()}
    BIT_PRECISION = {'smallint': 16, 'integer': 32, 'bigint': 64, 'real': 32, 'double': 64}


class ContainerType(SqlDataType):
    __module__ = __name__
    ATTRIBUTES = {'array': ['length'], 'composite': ()}


class ArrayType(ContainerType):
    __module__ = __name__


class CompositeType(ContainerType):
    __module__ = __name__


SIMPLE_TYPES = tuple(sorted(SimpleType.ATTRIBUTES.keys()))
CONTAINER_TYPES = tuple(sorted(ContainerType.ATTRIBUTES.keys()))
ALL_TYPES = tuple(sorted(SIMPLE_TYPES + CONTAINER_TYPES))
ns = Namespace(SQL_NAMESPACE_URI)
ns[None] = SimpleType
ns['array'] = ArrayType
ns['composite'] = CompositeType
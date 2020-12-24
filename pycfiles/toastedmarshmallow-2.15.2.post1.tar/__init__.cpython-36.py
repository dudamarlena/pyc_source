# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jphillips/go/src/github.com/lyft/toasted-marshmallow/toastedmarshmallow/__init__.py
# Compiled at: 2019-06-17 19:09:10
# Size of source mod 2**32: 662 bytes
from marshmallow import SchemaJit
from .jit import generate_marshall_method, generate_unmarshall_method, JitContext
__version__ = '2.15.1'

class Jit(SchemaJit):

    def __init__(self, schema):
        super(Jit, self).__init__(schema)
        self.schema = schema
        self.marshal_method = generate_marshall_method(schema,
          context=(JitContext()))
        self.unmarshal_method = generate_unmarshall_method(schema,
          context=(JitContext()))

    @property
    def jitted_marshal_method(self):
        return self.marshal_method

    @property
    def jitted_unmarshal_method(self):
        return self.unmarshal_method
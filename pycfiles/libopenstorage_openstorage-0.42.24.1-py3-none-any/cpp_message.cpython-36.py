# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/protobuf/google/protobuf/pyext/cpp_message.py
# Compiled at: 2020-01-10 16:25:26
# Size of source mod 2**32: 2851 bytes
"""Protocol message implementation hooks for C++ implementation.

Contains helper functions used to create protocol message classes from
Descriptor objects at runtime backed by the protocol buffer C++ API.
"""
__author__ = 'tibell@google.com (Johan Tibell)'
from google.protobuf.pyext import _message

class GeneratedProtocolMessageType(_message.MessageMeta):
    __doc__ = 'Metaclass for protocol message classes created at runtime from Descriptors.\n\n  The protocol compiler currently uses this metaclass to create protocol\n  message classes at runtime.  Clients can also manually create their own\n  classes at runtime, as in this example:\n\n  mydescriptor = Descriptor(.....)\n  factory = symbol_database.Default()\n  factory.pool.AddDescriptor(mydescriptor)\n  MyProtoClass = factory.GetPrototype(mydescriptor)\n  myproto_instance = MyProtoClass()\n  myproto.foo_field = 23\n  ...\n\n  The above example will not work for nested types. If you wish to include them,\n  use reflection.MakeClass() instead of manually instantiating the class in\n  order to create the appropriate class structure.\n  '
    _DESCRIPTOR_KEY = 'DESCRIPTOR'
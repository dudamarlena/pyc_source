# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/visionseed/FlasherParams_pb2.py
# Compiled at: 2019-08-19 03:18:21
# Size of source mod 2**32: 2193 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='FlasherParams.proto', package='', syntax='proto2', serialized_pb=_b('\n\x13FlasherParams.proto"*\n\rFlasherParams\x12\n\n\x02ir\x18\x01 \x01(\x05\x12\r\n\x05white\x18\x02 \x01(\x05'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_FLASHERPARAMS = _descriptor.Descriptor(name='FlasherParams', full_name='FlasherParams', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='ir', full_name='FlasherParams.ir', index=0, number=1, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='white', full_name='FlasherParams.white', index=1, number=2, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=23, serialized_end=65)
DESCRIPTOR.message_types_by_name['FlasherParams'] = _FLASHERPARAMS
FlasherParams = _reflection.GeneratedProtocolMessageType('FlasherParams', (_message.Message,), dict(DESCRIPTOR=_FLASHERPARAMS, __module__='FlasherParams_pb2'))
_sym_db.RegisterMessage(FlasherParams)
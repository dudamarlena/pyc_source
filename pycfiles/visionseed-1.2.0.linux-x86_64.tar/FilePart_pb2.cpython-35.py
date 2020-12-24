# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/visionseed/FilePart_pb2.py
# Compiled at: 2019-11-08 01:32:33
# Size of source mod 2**32: 2876 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='FilePart.proto', package='', syntax='proto2', serialized_pb=_b('\n\x0eFilePart.proto"K\n\x08FilePart\x12\x0c\n\x04path\x18\x01 \x02(\t\x12\x13\n\x0btotalLength\x18\x02 \x02(\x05\x12\x0e\n\x06offset\x18\x03 \x02(\x05\x12\x0c\n\x04data\x18\x04 \x02(\x0c'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_FILEPART = _descriptor.Descriptor(name='FilePart', full_name='FilePart', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='path', full_name='FilePart.path', index=0, number=1, type=9, cpp_type=9, label=2, has_default_value=False, default_value=_b('').decode('utf-8'), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='totalLength', full_name='FilePart.totalLength', index=1, number=2, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='offset', full_name='FilePart.offset', index=2, number=3, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='data', full_name='FilePart.data', index=3, number=4, type=12, cpp_type=9, label=2, has_default_value=False, default_value=_b(''), message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=18, serialized_end=93)
DESCRIPTOR.message_types_by_name['FilePart'] = _FILEPART
FilePart = _reflection.GeneratedProtocolMessageType('FilePart', (_message.Message,), dict(DESCRIPTOR=_FILEPART, __module__='FilePart_pb2'))
_sym_db.RegisterMessage(FilePart)
# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/protos/bipartite_matcher_pb2.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 1741 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/bipartite_matcher.proto', package='object_detection.protos', syntax='proto2', serialized_pb=_b('\n/object_detection/protos/bipartite_matcher.proto\x12\x17object_detection.protos"\x12\n\x10BipartiteMatcher'))
_BIPARTITEMATCHER = _descriptor.Descriptor(name='BipartiteMatcher', full_name='object_detection.protos.BipartiteMatcher', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=76, serialized_end=94)
DESCRIPTOR.message_types_by_name['BipartiteMatcher'] = _BIPARTITEMATCHER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
BipartiteMatcher = _reflection.GeneratedProtocolMessageType('BipartiteMatcher', (_message.Message,), dict(DESCRIPTOR=_BIPARTITEMATCHER, __module__='object_detection.protos.bipartite_matcher_pb2'))
_sym_db.RegisterMessage(BipartiteMatcher)
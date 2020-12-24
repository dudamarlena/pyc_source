# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/object_detection/protos/mean_stddev_box_coder_pb2.py
# Compiled at: 2018-06-15 01:39:54
# Size of source mod 2**32: 1777 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/mean_stddev_box_coder.proto', package='object_detection.protos', syntax='proto2', serialized_pb=_b('\n3object_detection/protos/mean_stddev_box_coder.proto\x12\x17object_detection.protos"\x14\n\x12MeanStddevBoxCoder'))
_MEANSTDDEVBOXCODER = _descriptor.Descriptor(name='MeanStddevBoxCoder', full_name='object_detection.protos.MeanStddevBoxCoder', filename=None, file=DESCRIPTOR, containing_type=None, fields=[], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=80, serialized_end=100)
DESCRIPTOR.message_types_by_name['MeanStddevBoxCoder'] = _MEANSTDDEVBOXCODER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
MeanStddevBoxCoder = _reflection.GeneratedProtocolMessageType('MeanStddevBoxCoder', (_message.Message,), dict(DESCRIPTOR=_MEANSTDDEVBOXCODER, __module__='object_detection.protos.mean_stddev_box_coder_pb2'))
_sym_db.RegisterMessage(MeanStddevBoxCoder)
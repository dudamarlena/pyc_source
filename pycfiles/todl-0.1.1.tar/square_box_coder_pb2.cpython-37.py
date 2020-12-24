# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/svpino/dev/tensorflow-object-detection-sagemaker/todl/tensorflow-object-detection/research/object_detection/protos/square_box_coder_pb2.py
# Compiled at: 2020-04-05 21:16:38
# Size of source mod 2**32: 2958 bytes
import google.protobuf as _descriptor
import google.protobuf as _message
import google.protobuf as _reflection
import google.protobuf as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='object_detection/protos/square_box_coder.proto',
  package='object_detection.protos',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=b'\n.object_detection/protos/square_box_coder.proto\x12\x17object_detection.protos"S\n\x0eSquareBoxCoder\x12\x13\n\x07y_scale\x18\x01 \x01(\x02:\x0210\x12\x13\n\x07x_scale\x18\x02 \x01(\x02:\x0210\x12\x17\n\x0clength_scale\x18\x03 \x01(\x02:\x015')
_SQUAREBOXCODER = _descriptor.Descriptor(name='SquareBoxCoder',
  full_name='object_detection.protos.SquareBoxCoder',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='y_scale',
   full_name='object_detection.protos.SquareBoxCoder.y_scale',
   index=0,
   number=1,
   type=2,
   cpp_type=6,
   label=1,
   has_default_value=True,
   default_value=(float(10)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='x_scale',
   full_name='object_detection.protos.SquareBoxCoder.x_scale',
   index=1,
   number=2,
   type=2,
   cpp_type=6,
   label=1,
   has_default_value=True,
   default_value=(float(10)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='length_scale',
   full_name='object_detection.protos.SquareBoxCoder.length_scale',
   index=2,
   number=3,
   type=2,
   cpp_type=6,
   label=1,
   has_default_value=True,
   default_value=(float(5)),
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR)],
  extensions=[],
  nested_types=[],
  enum_types=[],
  serialized_options=None,
  is_extendable=False,
  syntax='proto2',
  extension_ranges=[],
  oneofs=[],
  serialized_start=75,
  serialized_end=158)
DESCRIPTOR.message_types_by_name['SquareBoxCoder'] = _SQUAREBOXCODER
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
SquareBoxCoder = _reflection.GeneratedProtocolMessageType('SquareBoxCoder', (_message.Message,), {'DESCRIPTOR':_SQUAREBOXCODER, 
 '__module__':'object_detection.protos.square_box_coder_pb2'})
_sym_db.RegisterMessage(SquareBoxCoder)
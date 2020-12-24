# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/linshuliang/work_baidu/tb-paddle/tb_paddle/proto/plugin_pr_curve_pb2.py
# Compiled at: 2020-01-08 07:01:22
# Size of source mod 2**32: 2420 bytes
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='tb_paddle/proto/plugin_pr_curve.proto',
  package='tb_paddle',
  syntax='proto3',
  serialized_options=None,
  serialized_pb=b'\n%tb_paddle/proto/plugin_pr_curve.proto\x12\ttb_paddle"<\n\x11PrCurvePluginData\x12\x0f\n\x07version\x18\x01 \x01(\x05\x12\x16\n\x0enum_thresholds\x18\x02 \x01(\rb\x06proto3')
_PRCURVEPLUGINDATA = _descriptor.Descriptor(name='PrCurvePluginData',
  full_name='tb_paddle.PrCurvePluginData',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='version',
   full_name='tb_paddle.PrCurvePluginData.version',
   index=0,
   number=1,
   type=5,
   cpp_type=1,
   label=1,
   has_default_value=False,
   default_value=0,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='num_thresholds',
   full_name='tb_paddle.PrCurvePluginData.num_thresholds',
   index=1,
   number=2,
   type=13,
   cpp_type=3,
   label=1,
   has_default_value=False,
   default_value=0,
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
  syntax='proto3',
  extension_ranges=[],
  oneofs=[],
  serialized_start=52,
  serialized_end=112)
DESCRIPTOR.message_types_by_name['PrCurvePluginData'] = _PRCURVEPLUGINDATA
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
PrCurvePluginData = _reflection.GeneratedProtocolMessageType('PrCurvePluginData', (_message.Message,), {'DESCRIPTOR':_PRCURVEPLUGINDATA, 
 '__module__':'tb_paddle.proto.plugin_pr_curve_pb2'})
_sym_db.RegisterMessage(PrCurvePluginData)
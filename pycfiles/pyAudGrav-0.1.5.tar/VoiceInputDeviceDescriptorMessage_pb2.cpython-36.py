# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/postlund/pyatv_dev/pyatv/pyatv/mrp/protobuf/VoiceInputDeviceDescriptorMessage_pb2.py
# Compiled at: 2019-09-30 07:18:14
# Size of source mod 2**32: 3320 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
from pyatv.mrp.protobuf import AudioFormatSettingsMessage_pb2 as pyatv_dot_mrp_dot_protobuf_dot_AudioFormatSettingsMessage__pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='pyatv/mrp/protobuf/VoiceInputDeviceDescriptorMessage.proto',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n:pyatv/mrp/protobuf/VoiceInputDeviceDescriptorMessage.proto\x1a3pyatv/mrp/protobuf/AudioFormatSettingsMessage.proto"y\n\x1aVoiceInputDeviceDescriptor\x12+\n\rdefaultFormat\x18\x01 \x01(\x0b2\x14.AudioFormatSettings\x12.\n\x10supportedFormats\x18\x02 \x03(\x0b2\x14.AudioFormatSettings')),
  dependencies=[
 pyatv_dot_mrp_dot_protobuf_dot_AudioFormatSettingsMessage__pb2.DESCRIPTOR])
_VOICEINPUTDEVICEDESCRIPTOR = _descriptor.Descriptor(name='VoiceInputDeviceDescriptor',
  full_name='VoiceInputDeviceDescriptor',
  filename=None,
  file=DESCRIPTOR,
  containing_type=None,
  fields=[
 _descriptor.FieldDescriptor(name='defaultFormat',
   full_name='VoiceInputDeviceDescriptor.defaultFormat',
   index=0,
   number=1,
   type=11,
   cpp_type=10,
   label=1,
   has_default_value=False,
   default_value=None,
   message_type=None,
   enum_type=None,
   containing_type=None,
   is_extension=False,
   extension_scope=None,
   serialized_options=None,
   file=DESCRIPTOR),
 _descriptor.FieldDescriptor(name='supportedFormats',
   full_name='VoiceInputDeviceDescriptor.supportedFormats',
   index=1,
   number=2,
   type=11,
   cpp_type=10,
   label=3,
   has_default_value=False,
   default_value=[],
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
  serialized_start=115,
  serialized_end=236)
_VOICEINPUTDEVICEDESCRIPTOR.fields_by_name['defaultFormat'].message_type = pyatv_dot_mrp_dot_protobuf_dot_AudioFormatSettingsMessage__pb2._AUDIOFORMATSETTINGS
_VOICEINPUTDEVICEDESCRIPTOR.fields_by_name['supportedFormats'].message_type = pyatv_dot_mrp_dot_protobuf_dot_AudioFormatSettingsMessage__pb2._AUDIOFORMATSETTINGS
DESCRIPTOR.message_types_by_name['VoiceInputDeviceDescriptor'] = _VOICEINPUTDEVICEDESCRIPTOR
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
VoiceInputDeviceDescriptor = _reflection.GeneratedProtocolMessageType('VoiceInputDeviceDescriptor', (_message.Message,), {'DESCRIPTOR':_VOICEINPUTDEVICEDESCRIPTOR, 
 '__module__':'pyatv.mrp.protobuf.VoiceInputDeviceDescriptorMessage_pb2'})
_sym_db.RegisterMessage(VoiceInputDeviceDescriptor)
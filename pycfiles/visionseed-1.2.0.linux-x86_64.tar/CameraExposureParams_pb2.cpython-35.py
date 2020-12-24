# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/dist-packages/visionseed/CameraExposureParams_pb2.py
# Compiled at: 2019-11-08 01:32:33
# Size of source mod 2**32: 3973 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
from google.protobuf import descriptor_pb2
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='CameraExposureParams.proto', package='', syntax='proto2', serialized_pb=_b('\n\x1aCameraExposureParams.proto"\x9b\x01\n\x14CameraExposureParams\x12\r\n\x05camId\x18\x01 \x02(\x05\x120\n\x04type\x18\x02 \x02(\x0e2".CameraExposureParams.ExposureType\x12\x0e\n\x06timeUs\x18\x03 \x01(\x05\x12\x0c\n\x04gain\x18\x04 \x01(\x05"$\n\x0cExposureType\x12\n\n\x06MANUAL\x10\x00\x12\x08\n\x04AUTO\x10\x01'))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
_CAMERAEXPOSUREPARAMS_EXPOSURETYPE = _descriptor.EnumDescriptor(name='ExposureType', full_name='CameraExposureParams.ExposureType', filename=None, file=DESCRIPTOR, values=[
 _descriptor.EnumValueDescriptor(name='MANUAL', index=0, number=0, options=None, type=None),
 _descriptor.EnumValueDescriptor(name='AUTO', index=1, number=1, options=None, type=None)], containing_type=None, options=None, serialized_start=150, serialized_end=186)
_sym_db.RegisterEnumDescriptor(_CAMERAEXPOSUREPARAMS_EXPOSURETYPE)
_CAMERAEXPOSUREPARAMS = _descriptor.Descriptor(name='CameraExposureParams', full_name='CameraExposureParams', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='camId', full_name='CameraExposureParams.camId', index=0, number=1, type=5, cpp_type=1, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='type', full_name='CameraExposureParams.type', index=1, number=2, type=14, cpp_type=8, label=2, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='timeUs', full_name='CameraExposureParams.timeUs', index=2, number=3, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='gain', full_name='CameraExposureParams.gain', index=3, number=4, type=5, cpp_type=1, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[
 _CAMERAEXPOSUREPARAMS_EXPOSURETYPE], options=None, is_extendable=False, syntax='proto2', extension_ranges=[], oneofs=[], serialized_start=31, serialized_end=186)
_CAMERAEXPOSUREPARAMS.fields_by_name['type'].enum_type = _CAMERAEXPOSUREPARAMS_EXPOSURETYPE
_CAMERAEXPOSUREPARAMS_EXPOSURETYPE.containing_type = _CAMERAEXPOSUREPARAMS
DESCRIPTOR.message_types_by_name['CameraExposureParams'] = _CAMERAEXPOSUREPARAMS
CameraExposureParams = _reflection.GeneratedProtocolMessageType('CameraExposureParams', (_message.Message,), dict(DESCRIPTOR=_CAMERAEXPOSUREPARAMS, __module__='CameraExposureParams_pb2'))
_sym_db.RegisterMessage(CameraExposureParams)
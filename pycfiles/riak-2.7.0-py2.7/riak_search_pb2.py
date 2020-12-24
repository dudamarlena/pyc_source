# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/pb/riak_search_pb2.py
# Compiled at: 2016-12-06 18:54:22
from six import *
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import descriptor_pb2
import riak.pb.riak_pb2
DESCRIPTOR = _descriptor.FileDescriptor(name='riak_search.proto', package='', serialized_pb=b'\n\x11riak_search.proto\x1a\nriak.proto"(\n\x0cRpbSearchDoc\x12\x18\n\x06fields\x18\x01 \x03(\x0b2\x08.RpbPair"\x9d\x01\n\x11RpbSearchQueryReq\x12\t\n\x01q\x18\x01 \x02(\x0c\x12\r\n\x05index\x18\x02 \x02(\x0c\x12\x0c\n\x04rows\x18\x03 \x01(\r\x12\r\n\x05start\x18\x04 \x01(\r\x12\x0c\n\x04sort\x18\x05 \x01(\x0c\x12\x0e\n\x06filter\x18\x06 \x01(\x0c\x12\n\n\x02df\x18\x07 \x01(\x0c\x12\n\n\x02op\x18\x08 \x01(\x0c\x12\n\n\x02fl\x18\t \x03(\x0c\x12\x0f\n\x07presort\x18\n \x01(\x0c"W\n\x12RpbSearchQueryResp\x12\x1b\n\x04docs\x18\x01 \x03(\x0b2\r.RpbSearchDoc\x12\x11\n\tmax_score\x18\x02 \x01(\x02\x12\x11\n\tnum_found\x18\x03 \x01(\rB\'\n\x17com.basho.riak.protobufB\x0cRiakSearchPB')
_RPBSEARCHDOC = _descriptor.Descriptor(name='RpbSearchDoc', full_name='RpbSearchDoc', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='fields', full_name='RpbSearchDoc.fields', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=33, serialized_end=73)
_RPBSEARCHQUERYREQ = _descriptor.Descriptor(name='RpbSearchQueryReq', full_name='RpbSearchQueryReq', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='q', full_name='RpbSearchQueryReq.q', index=0, number=1, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='index', full_name='RpbSearchQueryReq.index', index=1, number=2, type=12, cpp_type=9, label=2, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='rows', full_name='RpbSearchQueryReq.rows', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='start', full_name='RpbSearchQueryReq.start', index=3, number=4, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='sort', full_name='RpbSearchQueryReq.sort', index=4, number=5, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='filter', full_name='RpbSearchQueryReq.filter', index=5, number=6, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='df', full_name='RpbSearchQueryReq.df', index=6, number=7, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='op', full_name='RpbSearchQueryReq.op', index=7, number=8, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='fl', full_name='RpbSearchQueryReq.fl', index=8, number=9, type=12, cpp_type=9, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='presort', full_name='RpbSearchQueryReq.presort', index=9, number=10, type=12, cpp_type=9, label=1, has_default_value=False, default_value='', message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=76, serialized_end=233)
_RPBSEARCHQUERYRESP = _descriptor.Descriptor(name='RpbSearchQueryResp', full_name='RpbSearchQueryResp', filename=None, file=DESCRIPTOR, containing_type=None, fields=[
 _descriptor.FieldDescriptor(name='docs', full_name='RpbSearchQueryResp.docs', index=0, number=1, type=11, cpp_type=10, label=3, has_default_value=False, default_value=[], message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='max_score', full_name='RpbSearchQueryResp.max_score', index=1, number=2, type=2, cpp_type=6, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None),
 _descriptor.FieldDescriptor(name='num_found', full_name='RpbSearchQueryResp.num_found', index=2, number=3, type=13, cpp_type=3, label=1, has_default_value=False, default_value=0, message_type=None, enum_type=None, containing_type=None, is_extension=False, extension_scope=None, options=None)], extensions=[], nested_types=[], enum_types=[], options=None, is_extendable=False, extension_ranges=[], serialized_start=235, serialized_end=322)
_RPBSEARCHDOC.fields_by_name['fields'].message_type = riak.pb.riak_pb2._RPBPAIR
_RPBSEARCHQUERYRESP.fields_by_name['docs'].message_type = _RPBSEARCHDOC
DESCRIPTOR.message_types_by_name['RpbSearchDoc'] = _RPBSEARCHDOC
DESCRIPTOR.message_types_by_name['RpbSearchQueryReq'] = _RPBSEARCHQUERYREQ
DESCRIPTOR.message_types_by_name['RpbSearchQueryResp'] = _RPBSEARCHQUERYRESP

@add_metaclass(_reflection.GeneratedProtocolMessageType)
class RpbSearchDoc(_message.Message):
    DESCRIPTOR = _RPBSEARCHDOC


@add_metaclass(_reflection.GeneratedProtocolMessageType)
class RpbSearchQueryReq(_message.Message):
    DESCRIPTOR = _RPBSEARCHQUERYREQ


@add_metaclass(_reflection.GeneratedProtocolMessageType)
class RpbSearchQueryResp(_message.Message):
    DESCRIPTOR = _RPBSEARCHQUERYRESP


DESCRIPTOR.has_options = True
DESCRIPTOR._options = _descriptor._ParseOptions(descriptor_pb2.FileOptions(), '\n\x17com.basho.riak.protobufB\x0cRiakSearchPB')
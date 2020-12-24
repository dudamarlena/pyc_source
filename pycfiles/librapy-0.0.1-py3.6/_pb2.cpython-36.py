# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/librapy/proto/_pb2.py
# Compiled at: 2019-09-06 14:49:44
# Size of source mod 2**32: 753 bytes
import sys
_b = sys.version_info[0] < 3 and (lambda x: x) or (lambda x: x.encode('latin1'))
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from google.protobuf import reflection as _reflection
from google.protobuf import symbol_database as _symbol_database
_sym_db = _symbol_database.Default()
DESCRIPTOR = _descriptor.FileDescriptor(name='librapy/proto/',
  package='',
  syntax='proto2',
  serialized_options=None,
  serialized_pb=(_b('\n\x0elibrapy/proto/')))
_sym_db.RegisterFileDescriptor(DESCRIPTOR)
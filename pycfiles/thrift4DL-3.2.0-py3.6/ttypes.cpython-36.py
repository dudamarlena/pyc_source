# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/thrift4DL/server/tcp/ttypes.py
# Compiled at: 2020-01-12 21:21:44
# Size of source mod 2**32: 439 bytes
from thrift.Thrift import TType, TMessageType, TFrozenDict, TException, TApplicationException
from thrift.protocol.TProtocol import TProtocolException
from thrift.TRecursive import fix_spec
import sys
from thrift.transport import TTransport
all_structs = []
fix_spec(all_structs)
del all_structs
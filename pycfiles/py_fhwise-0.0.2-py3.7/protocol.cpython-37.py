# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/fhwise/protocol.py
# Compiled at: 2019-09-27 12:41:56
# Size of source mod 2**32: 352 bytes
from construct import Struct, Bytes, Const, Int8ub, Int16ub, Rebuild, len_, this
Message = Struct('header' / Const(bytes.fromhex('7E7E')), 'length' / Rebuild(Int16ub, len_(this.payload) + 4), 'code' / Int8ub, 'payload' / Bytes(this.length - 4), 'cmdid' / Int8ub, 'end' / Const(bytes.fromhex('0D0A')))
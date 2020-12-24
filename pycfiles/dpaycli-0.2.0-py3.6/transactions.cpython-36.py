# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/dpayclibase/transactions.py
# Compiled at: 2018-10-14 23:35:20
# Size of source mod 2**32: 801 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
from binascii import hexlify, unhexlify
import struct
from dpaycligraphenebase.account import PublicKey
from .signedtransactions import Signed_Transaction
from .operations import Op_wrapper, Account_create

def getBlockParams(ws):
    """ Auxiliary method to obtain ``ref_block_num`` and
        ``ref_block_prefix``. Requires a websocket connection to a
        witness node!
    """
    dynBCParams = ws.get_dynamic_global_properties()
    ref_block_num = dynBCParams['head_block_number'] & 65535
    ref_block_prefix = struct.unpack_from('<I', unhexlify(dynBCParams['head_block_id']), 4)[0]
    return (ref_block_num, ref_block_prefix)
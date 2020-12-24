# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexstorebase/signedtransactions.py
# Compiled at: 2019-03-20 04:13:33
# Size of source mod 2**32: 695 bytes
from graphenebase.signedtransactions import Signed_Transaction as GrapheneSigned_Transaction
from .chains import known_chains
from .operations import Operation

class Signed_Transaction(GrapheneSigned_Transaction):
    __doc__ = ' Create a signed transaction and offer method to create the\n        signature\n\n        :param num refNum: parameter ref_block_num (see ``getBlockParams``)\n        :param num refPrefix: parameter ref_block_prefix (see ``getBlockParams``)\n        :param str expiration: expiration date\n        :param Array operations:  array of operations\n    '
    known_chains = known_chains
    default_prefix = 'DST'
    operation_klass = Operation
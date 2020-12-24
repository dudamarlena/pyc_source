# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/Run.py
# Compiled at: 2019-12-04 14:58:46
# Size of source mod 2**32: 231 bytes
from lds_merkle_proof_2019 import merkle_proof_2019
mp2019 = merkle_proof_2019.MerkleProof2019()
decoded_value = mp2019.decode('asdfasdf')
print(decoded_value)
encoded_value = mp2019.encode('{"test": true}')
print(encoded_value)
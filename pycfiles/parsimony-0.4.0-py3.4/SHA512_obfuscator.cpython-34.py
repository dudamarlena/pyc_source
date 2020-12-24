# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/parsimony/persistence/SHA512_obfuscator.py
# Compiled at: 2014-11-27 11:15:33
# Size of source mod 2**32: 620 bytes
import hashlib
from .data_obfuscator import DataObfuscator

class SHA512Obfuscator(DataObfuscator):
    __doc__ = 'DataObfuscator that uses the SHA512 hashing mechanism.\n\n    '

    def __init__(self):
        """
        """
        super(SHA512Obfuscator, self).__init__()

    def obfuscate(self, data):
        """Generate SHA512 of the hashable data representation

        :param data: data to obfuscate
        :return: hash
        """
        hashable_representation = self._hashable_representation(data)
        hasher = hashlib.sha512()
        hasher.update(hashable_representation)
        return hasher.digest()
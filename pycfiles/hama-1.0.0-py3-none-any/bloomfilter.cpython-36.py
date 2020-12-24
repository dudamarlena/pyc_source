# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/seongminnpark/hama-py/src/hama/dict/bloomfilter.py
# Compiled at: 2020-03-27 13:22:29
# Size of source mod 2**32: 1632 bytes
from .bitarray import BitArray
import mmh3, os

class LookupBloomFilter:
    __doc__ = 'Class representing bloom filters.\n\n    Bloom filters will represent morpheme \n    dictionaries and graphs.\n\n    Attributes:\n        bits: BitArray object representing the filter.\n        path: Path to byte array on disk.\n        size: Size of the BitArray.\n        hash_count: Number of hash functions used by this filter.\n    '

    def __init__(self, path, size, hash_count):
        super().__init__()
        self.path = path
        self.size = size
        self.hash_count = hash_count

    def __getattr__(self, name):
        """Called when an called attribute does not exist."""
        pass

    def load(self):
        """Read filter files from disk."""
        if self.bits is None:
            bit_path = os.path.join(os.path.dirname(__file__), 'bits', self.path)
            self.bits = BitArray(self.size)
            self.bits.read(bit_path)

    def query(self, item):
        """Queries item from the filter.

        Args:
            item (str): String to query.
           
        Returns: 
            bool: True if contains, False if not.

        Raises:
            Exception if bit array was not initialized
            before with load()
        """
        if self.bits is None:
            raise Exception('Initialize filter before querying!')
        for i in range(self.hash_count):
            hash = mmh3.hash(item, i) % self.size
            if self.bits.at(hash) == 0:
                return False

        return True
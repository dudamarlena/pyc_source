# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/migrate_tool/bloomfilter.py
# Compiled at: 2017-03-29 00:21:31
from hashlib import sha256
import json

class BloomFilter(object):
    """A simple bloom filter"""

    def __init__(self, array_size=1024, hashes=13):
        """Initializes a Filter() object
        Expects:
          array_size (in bytes): 4 * 1024 for a 4KB filter
          hashes (int): for the number of hashes to perform
        """
        self.filter = bytearray(array_size)
        self.bitcount = array_size * 8
        self.hashes = hashes

    def _hash(self, value):
        """Creates a hash of an int and yields a generator of hash functions
        Expects:
          value: int()
        Yields:
          generator of ints()
        """
        digest = int(sha256(value.__str__()).hexdigest(), 16)
        for _ in range(self.hashes):
            yield digest & self.bitcount - 1
            digest >>= 256 / self.hashes

    def add(self, value):
        """Bitwise OR to add value(s) into the self.filter
        Expects:
          value: generator of digest ints()
        """
        for digest in self._hash(value):
            self.filter[(digest / 8)] |= 2 ** (digest % 8)

    def query(self, value):
        """Bitwise AND to query values in self.filter
        Expects:
          value: value to check filter against (assumed int())
        """
        return all(self.filter[(digest / 8)] & 2 ** (digest % 8) for digest in self._hash(value))

    def loads(self, s):
        ret = json.loads(s)
        self.hashes = ret['hashes']
        self.bitcount = ret['bitcount']
        self.filter = bytearray(ret['filter'])

    def dumps(self):
        ret = dict()
        ret['hashes'] = self.hashes
        ret['bitcount'] = self.bitcount
        ret['filter'] = [ x for x in self.filter ]
        return json.dumps(ret)


if __name__ == '__main__':
    bf = BloomFilter()
    bf.add(1234)
    bf.add(40005)
    bf.add(1)
    bf.add('helloworld')
    bf.add('helloworldforevery')
    print ('Filter size {0} bytes').format(bf.filter.__sizeof__())
    print bf.query(1)
    print bf.query(40005)
    print bf.query(123)
    print bf.query('helloworld')
    print bf.query('hellomath')
    s = bf.dumps()
    bf2 = BloomFilter()
    bf2.loads(s)
    print bf2.query(1)
    print bf2.query(2)
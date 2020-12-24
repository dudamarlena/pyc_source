# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pykafka/partitioners.py
# Compiled at: 2018-05-14 12:02:28
# Size of source mod 2**32: 5870 bytes
__doc__ = '\nAuthor: Keith Bourgoin, Emmett Butler\n'
__license__ = '\nCopyright 2015 Parse.ly, Inc.\n\nLicensed under the Apache License, Version 2.0 (the "License");\nyou may not use this file except in compliance with the License.\nYou may obtain a copy of the License at\n\n    http://www.apache.org/licenses/LICENSE-2.0\n\nUnless required by applicable law or agreed to in writing, software\ndistributed under the License is distributed on an "AS IS" BASIS,\nWITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.\nSee the License for the specific language governing permissions and\nlimitations under the License.\n'
__all__ = ['RandomPartitioner', 'BasePartitioner', 'HashingPartitioner',
 'hashing_partitioner', 'GroupHashingPartitioner']
import random
from hashlib import sha1

class BasePartitioner(object):
    """BasePartitioner"""

    def __call__(self, partitions, key=None):
        raise NotImplementedError('Subclasses must define their own  partitioner implementation')


class RandomPartitioner(BasePartitioner):
    """RandomPartitioner"""

    def __init__(self):
        self.idx = 0

    def __call__(self, partitions, key):
        self.idx = (self.idx + 1) % len(partitions)
        return partitions[self.idx]


class HashingPartitioner(BasePartitioner):
    """HashingPartitioner"""

    def __init__(self, hash_func=None):
        """
        :param hash_func: hash function (defaults to :func:`hash`), should return
            an `int`. If hash randomization (Python 2.7) is enabled, a custom
            hashing function should be defined that is consistent between
            interpreter restarts.
        :type hash_func: function
        """
        self.hash_func = hash_func
        if self.hash_func is None:
            self.hash_func = lambda k: int(sha1(k).hexdigest(), 16)

    def __call__(self, partitions, key):
        """
        :param partitions: The partitions from which to choose
        :type partitions: sequence of :class:`pykafka.base.BasePartition`
        :param key: Key used for routing
        :type key: Any hashable type if using the default :func:`hash`
            implementation, any valid value for your custom hash function
        :returns: A partition
        :rtype: :class:`pykafka.base.BasePartition`
        """
        if key is None:
            raise ValueError('key cannot be `None` when using hashing partitioner')
        partitions = sorted(partitions)
        return partitions[(abs(self.hash_func(key)) % len(partitions))]


hashing_partitioner = HashingPartitioner()

class GroupHashingPartitioner(BasePartitioner):
    """GroupHashingPartitioner"""

    def __init__(self, hash_func, group_size=1):
        """
        :param hash_func: A hash function
        :type hash_func: function
        :param group_size: Size of the partition group to assign to. For example, if there are 16 partitions, and we
            want to smooth the distribution of identical keys between a set of 4, use 4 as the group_size.
        :type group_size: Integer value between (0, total_partition_count)
        """
        self.hash_func = hash_func
        self.group_size = group_size
        if self.hash_func is None:
            raise ValueError('hash_func must be specified when using GroupHashingPartitioner')
        if self.group_size < 1:
            raise ValueError('group_size cannot be < 1 when using GroupHashingPartitioner')

    def __call__(self, partitions, key):
        """
        :param partitions: The partitions from which to choose
        :type partitions: sequence of :class:`pykafka.base.BasePartition`
        :param key: Key used for routing
        :type key: Any hashable type if using the default :func:`hash`
            implementation, any valid value for your custom hash function
        :returns: A partition
        :rtype: :class:`pykafka.base.BasePartition`
        """
        if key is None:
            raise ValueError('key cannot be `None` when using hashing partitioner')
        if self.group_size > len(partitions):
            raise ValueError('group_size cannot be > available partitions')
        partitions = sorted(partitions)
        return partitions[(abs(self.hash_func(key) + random.randrange(0, self.group_size)) % len(partitions))]
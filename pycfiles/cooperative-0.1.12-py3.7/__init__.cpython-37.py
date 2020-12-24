# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/cooperative/__init__.py
# Compiled at: 2015-05-25 03:34:59
# Size of source mod 2**32: 3054 bytes
from collections import deque
from cooperative import _meta
__version__ = _meta.version
__version_info__ = _meta.version_info
from twisted.internet.task import cooperate
from stream_tap import stream_tap
from iter_karld_tools import i_batch

class ValueBucket(object):
    __doc__ = '\n    Produces a callable that accumulates all non-None values\n    it is called with in order.\n\n    The contents may be accessed or collected and drained,\n    to make room for new content.\n    '

    def __init__(self):
        self._contents = deque()

    def __call__(self, value):
        if value is not None:
            self._contents.append(value)

    def contents(self):
        """
        :returns: contents
        """
        return self._contents

    def drain_contents(self):
        """
        Starts a new collection to accumulate future contents
        and returns all of existing contents.
        """
        existing_contents = self._contents
        self._contents = deque()
        return existing_contents


def accumulation_handler(stopped_generator, spigot):
    """
    Drain the contents of the bucket from the spigot.

    :param stopped_generator: Generator which as stopped
    :param spigot: a Bucket.
    :return: The contents of the bucket.
    """
    return spigot.drain_contents()


def accumulate(a_generator, cooperator=None):
    """
    Start a Deferred whose callBack arg is a deque of the accumulation
    of the values yielded from a_generator.

    :param a_generator: An iterator which yields some not None values.
    :return: A Deferred to which the next callback will be called with
     the yielded contents of the generator function.
    """
    if cooperator:
        own_cooperate = cooperator.cooperate
    else:
        own_cooperate = cooperate
    spigot = ValueBucket()
    items = stream_tap((spigot,), a_generator)
    d = own_cooperate(items).whenDone()
    d.addCallback(accumulation_handler, spigot)
    return d


def batch_accumulate(max_batch_size, a_generator, cooperator=None):
    """
    Start a Deferred whose callBack arg is a deque of the accumulation
    of the values yielded from a_generator which is iterated over
    in batches the size of max_batch_size.

    It should be more efficient to iterate over the generator in
     batches and still provide enough speed for non-blocking execution.

    :param max_batch_size: The number of iterations of the generator
     to consume at a time.
    :param a_generator: An iterator which yields some not None values.
    :return: A Deferred to which the next callback will be called with
     the yielded contents of the generator function.
    """
    if cooperator:
        own_cooperate = cooperator.cooperate
    else:
        own_cooperate = cooperate
    spigot = ValueBucket()
    items = stream_tap((spigot,), a_generator)
    d = own_cooperate(i_batch(max_batch_size, items)).whenDone()
    d.addCallback(accumulation_handler, spigot)
    return d
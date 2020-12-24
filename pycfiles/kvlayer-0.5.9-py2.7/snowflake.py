# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/snowflake.py
# Compiled at: 2015-07-31 13:31:44
"""Snowflake key generator.

.. This software is released under an MIT/X11 open source license.
   Copyright 2015 Diffeo, Inc.

.. autoclass:: Snowflake

"""
from __future__ import absolute_import, division, print_function
import math, random, time

class Snowflake(object):
    """Snowflake key generator.

    This is a callable object that returns :class:`long` values
    that can be used as :mod:`kvlayer` keys.  These keys have the
    property that the most-recently-written keys appear first in a
    table scan, and that different hosts will probably write
    differently-valued keys.

    The keys are made up from the current timestamp, an
    object-specific identifier, and a sequence number.  For best
    results a single key generator should be shared across all parts
    of a single task or program.  For instance, if this is used in
    connection with :mod:`rejester`, the low-order bits of the current
    worker ID could be used to generate the initial identifier and
    sequence number.

    .. see:: https://blog.twitter.com/2010/announcing-snowflake

    """

    def __init__(self, identifier=None, sequence=None):
        if identifier is None:
            identifier = random.randint(0, 65535)
        if sequence is None:
            sequence = random.randint(0, 65535)
        self.identifier = identifier
        self.sequence = sequence
        return

    def __call__(self, now=None):
        if now is None:
            now = time.time()
        key = long((-math.trunc(now) & 2147483647) << 32 | (self.identifier & 65535) << 16 | self.sequence & 65535)
        self.sequence = self.sequence + 1 & 65535
        return key
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/__init__.py
# Compiled at: 2016-10-17 19:06:50
"""
The Riak API for Python allows you to connect to a Riak instance,
create, modify, and delete Riak objects, add and remove links from
Riak objects, run Javascript (and Erlang) based Map/Reduce
operations, and run Linkwalking operations.
"""
from riak.riak_error import RiakError, ConflictError
from riak.client import RiakClient
from riak.bucket import RiakBucket, BucketType
from riak.table import Table
from riak.node import RiakNode
from riak.riak_object import RiakObject
from riak.mapreduce import RiakKeyFilter, RiakMapReduce, RiakLink
__all__ = [
 'RiakBucket', 'Table', 'BucketType', 'RiakNode',
 'RiakObject', 'RiakClient', 'RiakMapReduce', 'RiakKeyFilter',
 'RiakLink', 'RiakError', 'ConflictError',
 'ONE', 'ALL', 'QUORUM', 'key_filter']
ONE = 'one'
ALL = 'all'
QUORUM = 'quorum'
key_filter = RiakKeyFilter()
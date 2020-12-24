# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: py-build/2.7/bdist.linux-x86_64/egg/riak/tests/yz_setup.py
# Compiled at: 2016-10-17 19:06:50
import logging
from riak import RiakError
from riak.tests import RUN_YZ
from riak.tests.base import IntegrationTestBase

def yzSetUp(*yzdata):
    if RUN_YZ:
        c = IntegrationTestBase.create_client()
        for yz in yzdata:
            logging.debug('yzSetUp: %s', yz)
            c.create_search_index(yz['index'], timeout=30000)
            if yz['btype'] is not None:
                t = c.bucket_type(yz['btype'])
                b = t.bucket(yz['bucket'])
            else:
                b = c.bucket(yz['bucket'])
            index_set = False
            while not index_set:
                try:
                    b.set_property('search_index', yz['index'])
                    index_set = True
                except RiakError:
                    pass

        c.close()
    return


def yzTearDown(c, *yzdata):
    if RUN_YZ:
        c = IntegrationTestBase.create_client()
        for yz in yzdata:
            logging.debug('yzTearDown: %s', yz)
            if yz['btype'] is not None:
                t = c.bucket_type(yz['btype'])
                b = t.bucket(yz['bucket'])
            else:
                b = c.bucket(yz['bucket'])
            b.set_property('search_index', '_dont_index_')
            c.delete_search_index(yz['index'])
            for keys in b.stream_keys():
                for key in keys:
                    b.delete(key)

        c.close()
    return
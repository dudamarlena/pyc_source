# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/tests/test_stats.py
# Compiled at: 2015-07-31 13:31:44
"""Basic functional tests for all of the kvlayer backends.

Your use of this software is governed by your license agreement.

Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import
import errno, logging, os, pdb, random, re, cStringIO as StringIO, sys, time, uuid, py, pytest, yaml
from pytest_diffeo import redis_address
import kvlayer
from kvlayer import BadKey
import yakonfig
logger = logging.getLogger(__name__)
backends = [
 'local', 'filestorage']
try:
    import psycopg2
    backends.append('postgres')
except ImportError as e:
    pass

@pytest.fixture(scope='module', params=backends)
def backend(request):
    return request.param


@pytest.yield_fixture(scope='function')
def client(backend, request, tmpdir, namespace_string):
    config_path = str(request.fspath.dirpath(('config_{0}.yaml').format(backend)))
    statsfile = StringIO.StringIO()
    params = dict(app_name='kvlayer', namespace=namespace_string, log_stats=statsfile, log_stats_interval_ops=1, blagh='hoo haa')
    if backend == 'filestorage':
        local = tmpdir.join('local')
        with local.open('w') as (f):
            pass
        params['kvlayer_filename'] = str(local)
    if backend == 'redis':
        params['storage_addresses'] = [
         redis_address(request)]
    with yakonfig.defaulted_config([kvlayer], filename=config_path, params=params):
        client = kvlayer.client()
        client.delete_namespace()
        yield client
        client.delete_namespace()


def test_stats(client):
    client.setup_namespace(dict(t1=(str, str), t2=(str, str, str)))
    assert 0 == len(list(client.scan('t1')))
    assert client._log_stats.scan.num_ops == 1
    assert client._log_stats.scan.by_table['t1'].num_ops == 1
    u1, u2, u3 = ('u1', 'u2', 'u3')
    client.put('t1', ((u1, u2), '88'))
    client.put('t2', ((u1, u2, u3), '88'))
    assert client._log_stats.put.num_ops == 2
    assert client._log_stats.put.by_table['t1'].num_ops == 1
    assert client._log_stats.put.by_table['t2'].num_ops == 1
    assert 1 == len(list(client.scan('t1')))
    assert 1 == len(list(client.scan('t1', ((u1,), (u1,)))))
    client.delete('t1', (u1, u2))
    assert client._log_stats.delete.num_ops == 1
    assert client._log_stats.delete.by_table['t1'].num_ops == 1
    assert client._log_stats.delete.by_table.get('t2') is None
    assert 0 == len(list(client.scan('t1')))
    assert 0 == len(list(client.scan('t1', ((u1,), (u1,)))))
    assert 0 == len(list(client.scan('t2', ((u2,), (u3,)))))
    assert client._log_stats.scan.num_ops == 6
    assert client._log_stats.scan.by_table['t1'].num_ops == 5
    assert client._log_stats.scan.by_table['t2'].num_ops == 1
    client._log_stats.flush()
    f = client._log_stats._f
    raw = f.getvalue()
    assert len(re.findall('put:', raw)) == 9
    logger.info('stats: %s', raw)
    client._log_stats.close()
    client._log_stats = None
    return
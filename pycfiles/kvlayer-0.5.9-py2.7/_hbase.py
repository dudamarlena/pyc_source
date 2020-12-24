# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_hbase.py
# Compiled at: 2015-07-31 13:31:44
"""
Implementation of AbstractStorage using HBase

Your use of this software is governed by your license agreement.

Copyright 2012-2015 Diffeo, Inc.
"""
import contextlib, logging, random, time, happybase as hbase
from kvlayer._exceptions import ProgrammerError
from kvlayer._abstract_storage import StringKeyedStorage
logger = logging.getLogger(__name__)

class HBaseStorage(StringKeyedStorage):
    """
    HBase storage implements kvlayer's AbstractStorage, which
    manages a set of tables as specified in setup_namespace
    """

    def __init__(self, *args, **kwargs):
        super(HBaseStorage, self).__init__(*args, **kwargs)
        addresses = self._config.get('storage_addresses', [])
        pool_size = self._config.get('pool_size', 10)
        if not addresses:
            raise ProgrammerError('config lacks storage_addresses')
        raddr = random.choice(addresses)
        logger.info('connecting to hbase thrift proxy: %r', raddr)
        prefix_sep = '_'
        prefix = '%s%s%s' % (self._app_name, prefix_sep, self._namespace)
        self._host, self._port = addr_port(raddr, 9090)
        self._pool = hbase.ConnectionPool(pool_size, host=self._host, port=self._port, table_prefix=prefix, table_prefix_separator=prefix_sep)
        self.max_batch_bytes = int(self._config.get('max_batch_bytes', 10000000))

    config_name = 'hbase'
    default_config = {'max_batch_bytes': 10000000}

    @contextlib.contextmanager
    def _conn(self):
        tries = 5
        for _ in xrange(tries):
            with self._pool.connection() as (conn):
                try:
                    conn.tables()
                except:
                    logger.warn('HBase connection is gone, maybe retrying...', exc_info=True)
                    conn._refresh_thrift_client()
                    time.sleep(0.5)
                    continue

                yield conn
                break

    def _create_table(self, table):
        with self._conn() as (conn):
            conn.create_table(table, {'d': dict(max_versions=1)})

    def setup_namespace(self, table_names, value_types={}):
        """creates tables in the namespace.  Can be run multiple times with
        different table_names in order to expand the set of tables in
        the namespace. This operation is idempotent.
        """
        super(HBaseStorage, self).setup_namespace(table_names, value_types)
        with self._conn() as (conn):
            existing_tables = conn.tables()
            for table in table_names:
                if table not in existing_tables:
                    self._create_table(table)

    def delete_namespace(self):
        """
        delete all of the tables within namespace
        """
        with self._conn() as (conn):
            for table in conn.tables():
                self._delete_table(table)

    def _delete_table(self, table_name):
        with self._conn() as (conn):
            conn.delete_table(table_name, disable=True)
            logger.debug('deleted table %s_%s_%s', self._app_name, self._namespace, table_name)

    def clear_table(self, table_name):
        self._delete_table(table_name)
        self._create_table(table_name)

    def _put(self, table_name, keys_and_values):
        with self._conn() as (conn):
            cur_bytes = 0
            table = conn.table(table_name)
            batch = table.batch()
            for key, blob in keys_and_values:
                morelen = len(blob) + len(key)
                if morelen + cur_bytes >= self.max_batch_bytes:
                    logger.debug('len(blob)=%d + cur_bytes=%d >= max_batch_bytes = %d', len(blob), cur_bytes, self.max_batch_bytes)
                    logger.debug('pre-emptively sending only what has been batched, and will send this item in next batch.')
                    batch.send()
                    batch = table.batch()
                    cur_bytes = 0
                batch.put(key, {'d:d': blob})
                cur_bytes += morelen

            if cur_bytes > 0:
                batch.send()

    def _scan(self, table_name, key_ranges):
        with self._conn() as (conn):
            if not key_ranges:
                key_ranges = [
                 [
                  '', '']]
            table = conn.table(table_name)
            for start_key, stop_key in key_ranges:
                if start_key or stop_key:
                    scanner = table.scan(row_start=start_key, row_stop=stop_key)
                else:
                    scanner = table.scan()
                for row in scanner:
                    yield (
                     row[0], row[1]['d:d'])

    def _scan_keys(self, table_name, key_ranges):
        with self._conn() as (conn):
            if not key_ranges:
                key_ranges = [
                 [
                  '', '']]
            table = conn.table(table_name)
            hfilter = 'KeyOnlyFilter()'
            for start_key, stop_key in key_ranges:
                if start_key or stop_key:
                    scanner = table.scan(row_start=start_key, row_stop=stop_key, columns=(), filter=hfilter)
                else:
                    scanner = table.scan(columns=(), filter=hfilter)
                for row in scanner:
                    yield row[0]

    def _get(self, table_name, keys):
        with self._conn() as (conn):
            table = conn.table(table_name)
            for key in keys:
                cf = table.row(key, columns=['d:d'])
                val = cf.get('d:d', None)
                yield (key, val)

        return

    def _delete(self, table_name, keys):
        with self._conn() as (conn):
            table = conn.table(table_name)
            batch = table.batch()
            for key in keys:
                batch.delete(key)

            batch.send()

    def close(self):
        pass

    def __del__(self):
        self.close()


def addr_port(addr, default_port):
    if ':' in addr:
        host, port = addr.split(':')
        return (
         host, int(port))
    else:
        return (
         addr, default_port)


def _string_decrement(x):
    if len(x) < 1:
        return
    else:
        pre = x[:-1]
        post = ord(x[(-1)])
        if post > 0:
            return pre + chr(post - 1) + b'\xff'
        pre = _string_decrement(pre)
        if pre is None:
            return
        return pre + b'\xff'
        return
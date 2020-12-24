# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_split_s3.py
# Compiled at: 2015-07-31 13:31:44
"""Split S3/kvlayer backend for kvlayer.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2015 Diffeo, Inc.

"""
from __future__ import absolute_import
import hashlib, time, boto, kvlayer
from kvlayer._abstract_storage import AbstractStorage
from kvlayer._exceptions import ConfigurationError

class SplitS3Storage(AbstractStorage):
    config_name = 'split_s3'
    default_config = {'path_prefix': '', 
       'kvlayer_prefix': True, 
       'retries': 5, 
       'retry_interval': 0.1}

    def __init__(self, *args, **kwargs):
        super(SplitS3Storage, self).__init__(*args, **kwargs)
        aws_access_key_id = self._value_or_path('aws_access_key_id')
        aws_secret_access_key = self._value_or_path('aws_secret_access_key')
        bucket_name = self._config.get('bucket', None)
        if not bucket_name:
            raise ConfigurationError('split_s3 storage requires bucket')
        self.tables = self._config.get('tables', None)
        if not self.tables:
            raise ConfigurationError('split_s3 storage requires tables')
        self.prefix = self._config.get('path_prefix', '')
        if self._config.get('kvlayer_prefix', True):
            self.prefix += ('{0}/{1}/').format(self._app_name, self._namespace)
        self.retries = self._config.get('retries', 5)
        self.retry_interval = self._config.get('retry_interval', 0.1)
        if 'kvlayer' not in self._config:
            raise ConfigurationError('split_s3 storage requires second kvlayer configuration')
        self.kvlclient = kvlayer.client(config=self._config['kvlayer'], app_name=self._app_name, namespace=self._namespace)
        connection = boto.connect_s3(aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key, is_secure=False)
        self.bucket = connection.get_bucket(bucket_name)
        return

    def _value_or_path(self, k):
        if k in self._config:
            return self._config[k]
        if k + '_path' in self._config:
            with open(self._config[(k + '_path')], 'r') as (f):
                return f.read().strip()
        raise ConfigurationError('split_s3 storage requires ' + k)

    def _s3_key(self, table_name, k):
        key = self._encoder.serialize_key(k, self._table_names[table_name])
        hasher = hashlib.sha256()
        hasher.update(key)
        key_hash = hasher.hexdigest()
        s3_key = ('{0}{1}/{2}/{3}/{4}').format(self.prefix, table_name, key_hash[0:2], key_hash[2:4], key_hash[4:])
        return self.bucket.new_key(s3_key)

    def setup_namespace(self, table_names, value_types):
        for t in table_names.iterkeys():
            if t not in self.tables:
                continue
            if t not in value_types:
                continue
            if value_types[t] is str:
                continue
            raise ConfigurationError(('table {0} is S3-backed but has non-string type {1!r}').format(t, value_types[t]))

        super(SplitS3Storage, self).setup_namespace(table_names, value_types)
        self.kvlclient.setup_namespace(table_names, value_types)

    def delete_namespace(self):
        """Deletes all data from all known tables.

        This iterates through known tables and individually deletes
        S3 objects, which may take some time.  It also deletes all data
        from the underlying kvlayer storage.

        """
        for t in self.tables:
            if t in self._table_names:
                self._clear_table(t)

        self.kvlclient.delete_namespace()

    def clear_table(self, table_name):
        """Deletes all data from a single table.

        This deletes both the underlying table and the S3 storage for
        every individual object in the table, if the table is backed by
        S3 storage.

        """
        if table_name in self.tables:
            self._clear_table(table_name)
        self.kvlclient.clear_table(table_name)

    def _clear_table(self, table_name):
        """Delete every known S3 object for a table.

        This scans the underlying kvlayer table to get keys, and issues
        S3 delete requests for them.

        """
        for k in self.kvlclient.scan_keys(table_name):
            self._s3_key(table_name, k).delete()

    def put(self, table_name, *keys_and_values, **kwargs):
        """Store objects in the underlying storage and maybe S3."""
        value_type = self._value_types[table_name]
        if table_name in self.tables:
            for k, v in keys_and_values:
                self.kvlclient.put(table_name, (k, ''), **kwargs)
                self._s3_key(table_name, k).set_contents_from_string(self.value_to_str(v, value_type))

        else:
            self.kvlclient.put(table_name, *keys_and_values, **kwargs)

    def _get(self, table_name, k):
        """Get a single object value from S3.

        This implements the retry logic.

        """
        tries_left = self.retries + 1
        key = self._s3_key(table_name, k)
        value = None
        while tries_left > 0:
            try:
                value = key.get_contents_as_string()
                break
            except Exception:
                if tries_left == 0:
                    raise

            tries_left -= 1
            time.sleep(self.retry_interval)

        if value is not None:
            return self.value_to_str(self._value_types[table_name])
        else:
            return

    def scan(self, table_name, *key_ranges, **kwargs):
        """Combination key/value scan.

        If you only need the keys, :meth:`scan_keys` won't access S3.

        """
        if table_name in self.tables:
            for k in self.kvlclient.scan_keys(table_name, *key_ranges, **kwargs):
                yield (
                 k, self._get(table_name, k))

        else:
            for kv in self.kvlclient.scan(table_name, *key_ranges, **kwargs):
                yield kv

    def scan_keys(self, table_name, *key_ranges, **kwargs):
        """Key-only scan.

        This is always a pass-through to the underlying kvlayer and
        never accesses S3.

        """
        return self.kvlclient.scan_keys(table_name, *key_ranges, **kwargs)

    def get(self, table_name, *keys, **kwargs):
        """Get specific keys."""
        for k, v0 in self.kvlclient.get(table_name, *keys, **kwargs):
            if v0 is not None and table_name in self.tables:
                v = self._get(table_name, k)
            else:
                v = v0
            yield (
             k, v)

        return

    def delete(self, table_name, *keys, **kwargs):
        """Delete specific keys."""
        if table_name in self.tables:
            for k in keys:
                self._s3_key(table_name, k).delete()

        self.kvlclient.delete(table_name, *keys, **kwargs)

    def close(self):
        """Shut down."""
        self.kvlclient.close()
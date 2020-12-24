# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/_riak.py
# Compiled at: 2015-07-31 13:31:44
"""kvlayer backend for Riak.

.. This software is released under an MIT/X11 open source license.
   Copyright 2014-2015 Diffeo, Inc.

"""
from __future__ import absolute_import
import riak
from kvlayer._abstract_storage import StringKeyedStorage

class RiakStorage(StringKeyedStorage):

    def __init__(self, *args, **kwargs):
        """Create a new Riak client object.

        This sets up a :class:`riak.RiakStorage` according to configuration,
        but in general this will not result in a network connection.

        """
        super(RiakStorage, self).__init__(*args, **kwargs)

        def make_node(s):
            if isinstance(s, basestring):
                return {'host': s}
            return s

        nodes = [ make_node(s) for s in self._config['storage_addresses'] ]
        self.connection = riak.RiakClient(protocol=self._config.get('protocol', 'pbc'), nodes=nodes)
        self.scan_limit = self._config.get('scan_limit', 100)

    def _bucket(self, table):
        """Riak bucket name for a kvlayer table."""
        name = ('{0}_{1}_{2}').format(self._app_name, self._namespace, table)
        return self.connection.bucket(name)

    def delete_namespace(self):
        """Deletes all data from the namespace.

        This only actually deletes keys in known namespaces, as per
        :meth:`setup_namespace`.  It needs to iterate and individually
        delete every single key.

        """
        for table in self._table_names.iterkeys():
            self.clear_table(table)

    def clear_table(self, table_name):
        """Deletes all data from a single table.

        This needs to iterate and delete every single key in the
        corresponding Riak bucket.

        """
        bucket = self._bucket(table_name)
        for k in bucket.get_keys():
            bucket.delete(k)

    def _put(self, table_name, keys_and_values):
        """Write some data to a table.

        Because of the way Riak works, each key/value pair is a separate
        write operation.  This backend makes no distinction between one
        write with multiple keys and multiple writes with one key.

        :param keys_and_values: data items to write
        :paramtype keys_and_values: pairs of (key, value)

        """
        bucket = self._bucket(table_name)
        for k, v in keys_and_values:
            obj = bucket.get(k)
            obj.encoded_data = v
            obj.content_type = 'application/octet-stream'
            obj.store()

    def _scan(self, table_name, key_ranges):
        """Scan key/value ranges from a table.

        This is not a native Riak operation!  It is implemented as an
        index scan, over the special index ``$key``.

        """
        return self._do_scan(table_name, key_ranges, with_values=True)

    def _scan_keys(self, table_name, key_ranges):
        """Scan key ranges from a table.

        This is not a native Riak operation!  It is implemented as an
        index scan, over the special index ``$key``.

        """
        return self._do_scan(table_name, key_ranges, with_values=False)

    def _do_scan(self, table_name, key_ranges, with_values=False):
        bucket = self._bucket(table_name)
        if not key_ranges:
            key_ranges = [
             (None, None)]
        for start_key, end_key in key_ranges:
            if not start_key:
                start_key = '\x00'
            if not end_key:
                end_key = b'\xff'
            results = bucket.get_index('$key', startkey=start_key, endkey=end_key, max_results=self.scan_limit)
            while True:
                for key in results:
                    obj = bucket.get(key)
                    if obj.exists:
                        if with_values:
                            yield (
                             key, obj.encoded_data)
                        else:
                            yield key

                if results.continuation:
                    results = results.next_page()
                else:
                    break

        return

    def _get(self, table_name, keys):
        """Yield tuples of (key, value) for specific keys."""
        bucket = self._bucket(table_name)
        for key in keys:
            obj = bucket.get(key)
            if obj.exists:
                yield (
                 key, obj.encoded_data)
            else:
                yield (
                 key, None)

        return

    def _delete(self, table_name, keys):
        """Delete some specific keys."""
        bucket = self._bucket(table_name)
        for key in keys:
            obj = bucket.get(key)
            obj.delete()

    def close(self):
        """End use of this storage client.

        While the Python Riak client maintains an internal connection
        pool, it is not exposed through the system API, and there is
        no obvious way to shut it down.

        """
        super(RiakStorage, self).close()
        self.connection = None
        return
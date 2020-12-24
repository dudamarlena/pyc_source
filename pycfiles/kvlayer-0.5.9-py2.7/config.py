# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kvlayer/config.py
# Compiled at: 2015-07-31 13:31:44
"""Configuration parameters for kvlayer.

These collectively implement the `yakonfig.Configurable` interface.

-----

This software is released under an MIT/X11 open source license.

Copyright 2012-2014 Diffeo, Inc.

"""
from __future__ import absolute_import
from kvlayer._client import STORAGE_CLIENTS
from yakonfig import ConfigurationError
config_name = 'kvlayer'
default_config = dict(storage_type='local', connection_pool_size=2, max_consistency_delay=120, replication_factor=1, thrift_framed_transport_size_in_mb=15, encoder='ascii_percent')

def add_arguments(parser):
    """Add command line arguments to an argparse.ArgumentParser instance."""
    parser.add_argument('--app-name', help='name of app for namespace prefixing')
    parser.add_argument('--namespace', help='namespace for prefixing table names')
    parser.add_argument('--storage-type', help='backend type for kvlayer, e.g. "local" or "accumulo"')
    parser.add_argument('--storage-address', action='append', dest='storage_addresses', metavar='HOST:PORT', help='network addresses for kvlayer, can be repeated')
    parser.add_argument('--username', help='username for kvlayer accumulo')
    parser.add_argument('--password', help='password for kvlayer accumulo')


runtime_keys = dict(app_name='app_name', namespace='namespace', username='username', password='password', storage_type='storage_type', storage_addresses='storage_addresses', connection_pool_size='connection_pool_size', max_consistency_delay='max_consistency_delay', replication_factor='replication_factor', thrift_framed_transport_size_in_mb='thrift_framed_transport_size_in_mb', log_stats='log_stats', log_stats_interval_ops='log_stats_interval_ops', log_stats_interval_seconds='log_stats_interval_seconds', kvlayer_filename='filename', kvlayer_copy_to_filename='copy_to_filename')

def discover_config(config, prefix):
    """Look out in the world to find kvlayer configuration.

    This will generally try to populate the `storage_type` and
    `storage_addresses` parameters, if a reasonable default for those
    can be found.

    """
    if 'storage_addresses' in config:
        return
    else:
        storage_type = config.get('storage_type', None)
        if storage_type is not None and storage_type in config and 'storage_addresses' in config[storage_type]:
            return
        for name in sorted(STORAGE_CLIENTS.iterkeys()):
            if storage_type is not None and storage_type != name:
                continue
            if name not in config:
                continue
            if 'storage_addresses' not in config[name]:
                continue
            if storage_type is None:
                config['storage_type'] = name
            return

        for name in sorted(STORAGE_CLIENTS.iterkeys()):
            if storage_type is not None and storage_type != name:
                continue
            impl = STORAGE_CLIENTS[name]
            if not hasattr(impl, 'discover_config'):
                continue
            sub_config = config.get(name, {})
            impl.discover_config(sub_config, prefix + '.' + name)
            if 'storage_addresses' not in sub_config:
                continue
            config[name] = sub_config
            if storage_type is None:
                config['storage_type'] = name
            return

        return


def check_config(config, name):
    if 'storage_type' not in config:
        raise ConfigurationError(('{0} must have a storage_type').format(name))
    if config['storage_type'] not in STORAGE_CLIENTS:
        raise ConfigurationError(('invalid {0} storage_type {1}').format(name, config['storage_type']))
    if 'namespace' not in config:
        raise ConfigurationError(('{0} requires a namespace').format(name))
    if 'app_name' not in config:
        raise ConfigurationError(('{0} requires an app_name').format(name))
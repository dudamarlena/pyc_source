# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/rejester/config.py
# Compiled at: 2015-07-08 07:32:10
""":mod:`yakonfig` declarations for rejester.

.. This software is released under an MIT/X11 open source license.
   Copyright 2012-2014 Diffeo, Inc.
"""
from __future__ import absolute_import
import os, yakonfig
config_name = 'rejester'
default_config = {'app_name': 'rejester', 
   'worker': 'fork_worker', 
   'enough_memory': False, 
   'default_lifetime': 1500}

def add_arguments(parser):
    parser.add_argument('--app-name', help='name of app for namespace prefixing')
    parser.add_argument('--namespace', help='namespace for prefixing table names')
    parser.add_argument('--registry-address', metavar='HOST:PORT', action='append', dest='registry_addresses', help='location of the Redis registry server')


runtime_keys = {'app_name': 'app_name', 
   'registry_addresses': 'registry_addresses', 
   'namespace': 'namespace'}

def discover_config(config, name):
    if 'registry_addresses' not in config:
        addr = os.environ.get('REDIS_PORT_6379_TCP_ADDR', None)
        port = os.environ.get('REDIS_PORT_6379_TCP_PORT', None)
        if addr and port:
            config['registry_addresses'] = [
             addr + ':' + port]
    return


def check_config(config, name):
    for k in ['registry_addresses', 'app_name', 'namespace']:
        if k not in config or config[k] is None:
            raise yakonfig.ConfigurationError(('{0} requires configuration for {1}').format(name, k))

    if len(config['registry_addresses']) == 0:
        raise yakonfig.ConfigurationError(('{0} requires at least one registry_addresses').format(name))
    for addr in config['registry_addresses']:
        if ':' not in addr:
            raise yakonfig.ConfigurationError(('{0} registry_addresses must be HOST:PORT, not {1!r}').format(name, addr))

    return
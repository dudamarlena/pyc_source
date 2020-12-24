# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/plugins/sproc/servers.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 1005 bytes
"""Syncronizes cell Zookeeper with LDAP data."""
from treadmill import admin
from treadmill import context
from treadmill import master

def sync_servers():
    """Sync servers and buckets."""
    admin_srv = admin.Server(context.GLOBAL.ldap.conn)
    servers = admin_srv.list({'cell': context.GLOBAL.cell})
    for server in servers:
        servername = server['_id']
        rack = 'rack:unknown'
        building = 'building:unknown'
        traits = []
        label = None
        master.create_bucket(context.GLOBAL.zk.conn, building, None)
        master.cell_insert_bucket(context.GLOBAL.zk.conn, building)
        master.create_bucket(context.GLOBAL.zk.conn, rack, building)
        master.create_server(context.GLOBAL.zk.conn, servername, rack)
        master.update_server_attrs(context.GLOBAL.zk.conn, servername, traits=traits, label=label)


def init():
    """Return top level command handler."""
    return sync_servers()
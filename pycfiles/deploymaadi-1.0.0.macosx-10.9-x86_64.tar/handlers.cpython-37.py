# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/maypatha/Workspace/Github/onlinejudge95/Popper/env/lib/python3.7/site-packages/deploymaadi/configure/handlers.py
# Compiled at: 2019-09-18 10:53:44
# Size of source mod 2**32: 371 bytes
from click import echo
from fabric import Connection

def init(ctx, cfg=None):
    if not cfg:
        raise ValueError('No config set, provide a config file.')
    host = cfg.get('host')
    user = cfg.get('user')
    echo(f"Connecting to {user} @ {host}")
    conn = Connection(host, user=user)
    conn.sudo('apt-get -y update')
    conn.sudo('apt-get -y upgrade')
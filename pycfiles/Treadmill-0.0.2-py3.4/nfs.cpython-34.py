# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/plugins/fs/nfs.py
# Compiled at: 2017-03-22 02:19:40
# Size of source mod 2**32: 373 bytes
"""Configures NFS inside the container."""

def init(rootdir):
    """Pre mount NFS shares for private nfs namespace to a Treadmill known
    location.

    This is done to avoid NFS delays at container create time."""
    del rootdir


def configure(approot, newroot, app):
    """Mounts nfs based on container environment."""
    del approot
    del newroot
    del app
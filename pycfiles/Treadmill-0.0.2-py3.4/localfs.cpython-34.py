# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/plugins/fs/localfs.py
# Compiled at: 2017-04-03 03:14:43
# Size of source mod 2**32: 795 bytes
"""Manage container filesystem layout."""
import os, stat
from treadmill import fs

def init(_rootdir):
    """Init filesystem layout."""
    pass


def configure(_approot, newroot, _app):
    """Configure layout in chroot."""
    newroot_norm = fs.norm_safe(newroot)
    mounts = []
    emptydirs = [
     '/u',
     '/var/account',
     '/var/empty',
     '/var/lock',
     '/var/log',
     '/var/run']
    stickydirs = [
     '/opt']
    for mount in mounts:
        if os.path.exists(mount):
            fs.mount_bind(newroot_norm, mount)
            continue

    for directory in emptydirs:
        fs.mkdir_safe(newroot_norm + directory)

    for directory in stickydirs:
        os.chmod(newroot_norm + directory, 777 | stat.S_ISVTX)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scripy/_path.py
# Compiled at: 2010-02-16 08:08:48
"""Absolute path of files."""

class Bin(object):
    """Avoid possible trojans into executables from a modified *PATH*."""
    chown = '/bin/chown'
    cp = '/bin/cp'
    grep = '/bin/grep'
    ls = '/bin/ls'
    readlink = '/bin/readlink'
    sed = '/bin/sed'
    modprobe = '/sbin/modprobe'
    apt_get = '/usr/bin/apt-get'
    diff = '/usr/bin/diff'
    find = '/usr/bin/find'
    stat = '/usr/bin/stat'
    sudo = '/usr/bin/sudo'
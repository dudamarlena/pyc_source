# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/whitlam/home/users/uqdparks/git/unitem/unitem/__init__.py
# Compiled at: 2017-06-13 17:58:37
import os

def version():
    """Read program version from file."""
    import unitem
    version_file = open(os.path.join(__path__[0], 'VERSION'))
    return version_file.readline().strip()
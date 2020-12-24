# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: vfclust/__init__.py
# Compiled at: 2014-06-25 21:50:36
"""
To setup (from terminal):
$ cd /path/to/vfclust/download
$ python setup.py install

>> import vfclust

For arguments and default values, see the README.md file.
"""
import sys
__author__ = 'Thomas Christie (tchristie@umn.edu), James Ryan, Serguei Pakhomov'
__copyright__ = 'Copyright (c) 2013-2014 Serguei Pakhomov'
__license__ = 'Apache License, Version 2.0'
__vcs_id__ = '$Id$'
__version__ = '0.1.0'
if __name__ == 'vfclust':
    from vfclust import *
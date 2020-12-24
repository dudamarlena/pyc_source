# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-intel/egg/tornetcd/__init__.py
# Compiled at: 2016-06-16 04:48:12
__author__ = 'mqingyn'
__version__ = '0.1.8'
version = tuple(map(int, __version__.split('.')))
from etcd_result import EtcdResult
from exceptions import *
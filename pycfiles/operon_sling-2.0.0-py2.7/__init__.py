# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sling/__init__.py
# Compiled at: 2019-02-05 06:56:06
from pkg_resources import get_distribution
try:
    __version__ = get_distribution('sling').version
except:
    __version__ = 'local'

__all__ = [
 'prepare',
 'scan',
 'filter',
 'group',
 'create_db',
 'tasks']
from sling import *
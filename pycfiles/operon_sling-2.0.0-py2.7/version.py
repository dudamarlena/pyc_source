# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/sling/tasks/version.py
# Compiled at: 2019-11-01 07:27:20
from sling import __version__ as sling_version
import sling

def run():
    print 'SLING verion: ' + str(sling_version)
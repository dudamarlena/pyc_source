# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/_nmf/__init__.py
# Compiled at: 2013-02-05 14:46:40
import pkg_resources

def datasets():
    yield (
     'nmf', pkg_resources.resource_filename(__name__, 'datasets'))
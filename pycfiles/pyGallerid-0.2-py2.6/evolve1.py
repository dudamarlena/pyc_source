# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/evolve/evolve1.py
# Compiled at: 2012-01-31 10:38:29
"""
repoze.evolution script for the pyGallerid database.
"""
from . import walk_resources

def evolve(context):
    for resource in walk_resources(context):
        cls = type(resource)
        if hasattr(cls, '__attributes__') and not hasattr(resource, '__attributes__'):
            resource.__attributes__ = cls.__attributes__
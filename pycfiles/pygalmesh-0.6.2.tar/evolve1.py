# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyGallerid/evolve/evolve1.py
# Compiled at: 2012-01-31 10:38:29
__doc__ = '\nrepoze.evolution script for the pyGallerid database.\n'
from . import walk_resources

def evolve(context):
    for resource in walk_resources(context):
        cls = type(resource)
        if hasattr(cls, '__attributes__') and not hasattr(resource, '__attributes__'):
            resource.__attributes__ = cls.__attributes__
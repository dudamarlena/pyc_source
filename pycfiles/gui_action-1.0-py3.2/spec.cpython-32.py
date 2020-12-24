# uncompyle6 version 3.7.4
# Python bytecode 3.2 (3180)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/gui/action/core/spec.py
# Compiled at: 2013-10-04 10:48:33
"""
Created on Sep 4, 2013

@package: gui action
@copyright: 2012 Sourcefabric o.p.s.
@license: http://www.gnu.org/licenses/gpl-3.0.txt
@author: Gabriel Nistor

Specifications and general functions for GUI action.
"""
from collections import Iterable

def listRootPaths(paths, start=0):
    """
    Iterates the root paths for the provided iterator.
    
    @param paths: Iterable(string)
        The paths to list the roots for.
    @param start: integer
        The start offset from where the root should be extracted.
    @return: list[string]
        The root paths.
    """
    assert isinstance(paths, Iterable), 'Invalid paths %s' % paths
    roots = set()
    for path in paths:
        assert isinstance(path, str), 'Invalid path %s' % path
        ipath = path.find('.', start)
        if ipath >= 0:
            roots.add(path[:ipath])
        else:
            roots.add(path)

    return sorted(roots)


def listCompletePaths(paths):
    """
    Iterates the paths for the provided iterator and completes the missing root paths.
    
    @param paths: Iterable(string)
        The paths to list the complete paths for.
    @return: list[string]
        The complete paths.
    """
    assert isinstance(paths, Iterable), 'Invalid paths %s' % paths
    allPaths = set()
    for path in paths:
        assert isinstance(path, str), 'Invalid path %s' % path
        items = []
        for item in path.split('.'):
            items.append(item)
            allPaths.add('.'.join(items))

    return sorted(allPaths)
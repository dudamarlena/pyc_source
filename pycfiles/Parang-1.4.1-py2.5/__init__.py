# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/parang/__init__.py
# Compiled at: 2009-08-22 22:50:09
"""Parang Diplomacy clients
    Copyright (C) 2003-2008  Eric Wald, David Norman, Andrew Huff, Vincent
    Chan, Laurence Tondelier, Damian Bundred, Colm Egan, and Neil Schemenauer
    
    Parang is a set of clients that can play the Diplomacy board game over
    a network, using the Parlance framework.
    
    This software may be reused for non-commercial purposes without charge,
    and without notifying the authors.  Use of any part of this software for
    commercial purposes without permission from the authors is prohibited.
"""

def __version__():
    """Tries to get a version number automatically, using setuptools.
        Defined first as a function to avoid leaking imported names.
    """
    try:
        from pkg_resources import get_distribution
        dist = get_distribution(__name__)
    except:
        version = None
    else:
        version = 'v' + dist.version

    return version


__version__ = __version__()
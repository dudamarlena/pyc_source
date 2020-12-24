# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/unidist/schemagen.py
# Compiled at: 2010-10-14 14:04:22
"""
schemagen

by Geoff Howland  <geoff AT ge01f DOT com>

TODO(g): Can hold and access all information in memory, and trade changes to
    other nodes, so all of a schema could be saved in sharedstate.  This
    way this system can truly become a memory based DB system too.  Just for
    kicks!
    
    Schemagen could keep in sync with a MySQLdb, or migrate data between them,
    or other DBs, by loading the entire schema in RAM (or parts of it, and
    rotating through as requested/needed to process everything within
    constraints of RAM.)
    
    This also makes schemagen a reddis/memcached-like machine, that can sync up
    with things.  Yay!  This is now also a NoSQL engine!  And it COMBINES with
    MySQL!  Best yet!  :)

TODO(g): Move to it's own module, when I create it.  This is just a placeholder.
    Messy, but whatever.  The place has been held!
"""
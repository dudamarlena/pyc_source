# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/s2616794/Documents/Projects/Uni/workspace_rdflib/rdflib-zodb/test/__init__.py
# Compiled at: 2014-02-26 17:10:12
from rdflib import plugin
from rdflib import store
plugin.register('ZODB', store.Store, 'rdflib_zodb.ZODB', 'ZODBStore')
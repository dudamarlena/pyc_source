# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dossier/web/tests/test_search_engines.py
# Compiled at: 2015-09-05 21:24:22
from __future__ import absolute_import, division, print_function
from dossier.fc import FeatureCollection
import dossier.web.search_engines as search_engines
from dossier.web.tests import config_local, kvl, store

def test_random_no_name_index(store):
    store.put([('foo', FeatureCollection({'NAME': {'bar': 1}}))])
    search_engines.random(store).set_query_id('foo').results()
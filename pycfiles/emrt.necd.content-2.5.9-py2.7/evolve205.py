# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve205.py
# Compiled at: 2019-02-15 13:51:23
import plone.api as api

def run(_):
    catalog = api.portal.get_tool('portal_catalog')
    indexes = ('observation_sent_to_msc', 'observation_sent_to_mse')
    catalog.reindexIndex(indexes, REQUEST=None)
    return
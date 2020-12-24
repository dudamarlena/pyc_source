# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/upgrades/evolve2010.py
# Compiled at: 2019-02-15 13:51:23
import plone.api as api
VOCABS = ('pollutants', 'fuel', 'conclusion_reasons')

def run(_):
    vocab_tool = api.portal.get_tool('portal_vocabularies')
    vocabs = tuple([ vocab_tool[name] for name in VOCABS ])
    api.content.delete(objects=vocabs)
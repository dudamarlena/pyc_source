# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/resource/testing.py
# Compiled at: 2009-06-03 06:44:54
"""
Created on 03.06.2009

@author: falko
"""
from zope.app.testing import setup
from falkolab.resource.util import ResourceTypesVocabulary

def setUp(test):
    test.globs = {'root': setup.placefulSetUp(True)}
    from zope.schema.vocabulary import getVocabularyRegistry
    registry = getVocabularyRegistry()
    registry.register('falkolab.resource.AvailableResourceTypes', ResourceTypesVocabulary)


def tearDown(test):
    setup.placefulTearDown()
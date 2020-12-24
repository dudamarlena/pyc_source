# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/workflow/vocabulary.py
# Compiled at: 2012-06-26 16:56:38
from zope.schema.interfaces import IVocabularyFactory
from interfaces import IWorkflow
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import classProvides

class WorkflowVocabulary(UtilityVocabulary):
    classProvides(IVocabularyFactory)
    interface = IWorkflow
    nameOnly = True
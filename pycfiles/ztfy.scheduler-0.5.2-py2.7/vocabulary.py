# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/vocabulary.py
# Compiled at: 2012-10-22 06:18:07
from zope.schema.interfaces import IVocabularyFactory
from ztfy.scheduler.interfaces import ISchedulerTaskSchedulingMode
from zope.componentvocabulary.vocabulary import UtilityVocabulary
from zope.interface import classProvides

class SchedulerTaskSchedulingModesVocabulary(UtilityVocabulary):
    """Scheduler tasks scheduling modes vocabulary"""
    classProvides(IVocabularyFactory)
    interface = ISchedulerTaskSchedulingMode
    nameOnly = True
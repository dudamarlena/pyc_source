# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/question_to_counterpart.py
# Compiled at: 2019-05-21 05:08:42
from Acquisition import aq_parent
from esdrt.content.question import IQuestion
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_cp(context, event):
    """
    To:     CounterParts
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('question_to_counterpart.pt')
    if event.action in ('phase1-request-for-counterpart-comments', 'phase2-request-for-counterpart-comments'):
        observation = aq_parent(context)
        subject = 'New draft question to comment'
        notify(observation, _temp, subject, role='CounterPart', notification_name='question_to_counterpart')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_qe(context, event):
    """
    To:     QualityExpert
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('question_to_counterpart.pt')
    if event.action in ('phase1-request-for-counterpart-comments', ):
        observation = aq_parent(context)
        subject = 'New draft question to comment'
        notify(observation, _temp, subject, role='QualityExpert', notification_name='question_to_counterpart')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('question_to_counterpart.pt')
    if event.action in ('phase2-request-for-counterpart-comments', ):
        observation = aq_parent(context)
        subject = 'New draft question to comment'
        notify(observation, _temp, subject, role='LeadReviewer', notification_name='question_to_counterpart')
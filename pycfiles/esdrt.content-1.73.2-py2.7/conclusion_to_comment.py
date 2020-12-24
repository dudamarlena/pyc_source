# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/conclusion_to_comment.py
# Compiled at: 2019-05-21 05:08:42
from esdrt.content.observation import IObservation
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_cp(context, event):
    """
    To:     CounterParts
    When:   New draft conclusion to comment on
    """
    _temp = PageTemplateFile('conclusion_to_comment.pt')
    if event.action in ('phase1-request-comments', 'phase2-request-comments'):
        observation = context
        subject = 'New draft conclusion to comment on'
        notify(observation, _temp, subject, 'CounterPart', 'conclusion_to_comment')


@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_qe(context, event):
    """
    To:     QualityExpert
    When:   New draft conclusion to comment on
    """
    _temp = PageTemplateFile('conclusion_to_comment.pt')
    if event.action in ('phase1-request-comments', ):
        observation = context
        subject = 'New draft conclusion to comment on'
        notify(observation, _temp, subject, 'QualityExpert', 'conclusion_to_comment')


@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('conclusion_to_comment.pt')
    if event.action in ('phase2-request-comments', ):
        observation = context
        subject = 'New draft conclusion to comment on'
        notify(observation, _temp, subject, 'LeadReviewer', 'conclusion_to_comment')
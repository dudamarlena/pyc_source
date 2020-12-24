# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/question_answered.py
# Compiled at: 2019-05-21 05:08:42
from Acquisition import aq_parent
from esdrt.content.question import IQuestion
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_qe(context, event):
    """
    To:     QualityExpert
    When:   New answer from country
    """
    _temp = PageTemplateFile('question_answered_lr_msg.pt')
    if event.action in ('phase1-answer-to-lr', ):
        observation = aq_parent(context)
        subject = 'New answer from country'
        notify(observation, _temp, subject, 'QualityExpert', 'question_answered')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New answer from country
    """
    _temp = PageTemplateFile('question_answered_lr_msg.pt')
    if event.action in ('phase2-answer-to-lr', ):
        observation = aq_parent(context)
        subject = 'New answer from country'
        notify(observation, _temp, subject, 'LeadReviewer', 'question_answered')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_rev_ph1(context, event):
    """
    To:     ReviewerPhase1
    When:   New answer from country
    """
    _temp = PageTemplateFile('question_answered_rev_msg.pt')
    if event.action in ('phase1-answer-to-lr', ):
        observation = aq_parent(context)
        subject = 'New answer from country'
        notify(observation, _temp, subject, 'ReviewerPhase1', 'question_answered')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_rev_ph2(context, event):
    """
    To:     ReviewerPhase2
    When:   New answer from country
    """
    _temp = PageTemplateFile('question_answered_rev_msg.pt')
    if event.action in ('phase2-answer-to-lr', ):
        observation = aq_parent(context)
        subject = 'New answer from country'
        notify(observation, _temp, subject, 'ReviewerPhase2', 'question_answered')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_rev_msexperts(context, event):
    """
    To:     MSExperts
    When:   New answer from country
    """
    _temp = PageTemplateFile('question_answered_msexperts_msg.pt')
    if event.action in ('phase1-answer-to-lr', 'phase2-answer-to-lr'):
        observation = aq_parent(context)
        subject = 'New answer from country'
        notify(observation, _temp, subject, 'MSExpert', 'question_answered')
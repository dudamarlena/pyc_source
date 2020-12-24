# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/question_ready_for_approval.py
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
    When:   New question for approval
    """
    _temp = PageTemplateFile('question_ready_for_approval.pt')
    if event.action in ('phase1-send-to-lr', ):
        observation = aq_parent(context)
        subject = 'New question for approval'
        notify(observation, _temp, subject, 'QualityExpert', 'question_ready_for_approval')


@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New question for approval
    """
    _temp = PageTemplateFile('question_ready_for_approval.pt')
    if event.action in ('phase2-send-to-lr', ):
        observation = aq_parent(context)
        subject = 'New question for approval'
        notify(observation, _temp, subject, 'LeadReviewer', 'question_ready_for_approval')
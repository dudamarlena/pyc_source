# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/question_ready_for_approval.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_LR

def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New question for approval
    """
    _temp = PageTemplateFile('question_ready_for_approval.pt')
    if event.action in ('send-to-lr', ):
        observation = aq_parent(context)
        subject = 'New question for approval'
        notify(observation, _temp, subject, ROLE_LR, 'question_ready_for_approval')
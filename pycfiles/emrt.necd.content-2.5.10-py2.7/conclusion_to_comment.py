# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/conclusion_to_comment.py
# Compiled at: 2019-02-15 13:51:23
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_CP
from emrt.necd.content.constants import ROLE_LR

def notification_cp(context, event):
    """
    To:     CounterParts
    When:   New draft conclusion to comment on
    """
    _temp = PageTemplateFile('conclusion_to_comment.pt')
    if event.action in ('request-comments', ):
        observation = context
        subject = 'New draft conclusion to comment on'
        notify(observation, _temp, subject, ROLE_CP, 'conclusion_to_comment')


def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   New draft question to comment on
    """
    _temp = PageTemplateFile('conclusion_to_comment.pt')
    if event.action in ('request-comments', ):
        observation = context
        subject = 'New draft conclusion to comment on'
        notify(observation, _temp, subject, ROLE_LR, 'conclusion_to_comment')
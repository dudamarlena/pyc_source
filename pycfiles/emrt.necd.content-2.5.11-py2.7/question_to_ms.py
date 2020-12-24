# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/question_to_ms.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_MSA
from emrt.necd.content.constants import ROLE_SE

def notification_ms(context, event):
    """
    To:     MSAuthority
    When:   New question for your country
    """
    _temp = PageTemplateFile('question_to_ms.pt')
    if event.action in ('approve-question', ):
        observation = aq_parent(context)
        subject = 'New question for your country'
        notify(observation, _temp, subject, role=ROLE_MSA, notification_name='question_to_ms')


def notification_se(context, event):
    """
    To:     SectorExpert
    When:   Your question was sent to MS
    """
    _temp = PageTemplateFile('question_to_ms_rev_msg.pt')
    if event.action in ('approve-question', ):
        observation = aq_parent(context)
        subject = 'Your observation was sent to MS'
        notify(observation, _temp, subject, role=ROLE_SE, notification_name='question_to_ms')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/answer_acknowledged.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_MSA

def notification_ms(context, event):
    """
    To:     MSAuthority
    When:   Answer Acknowledged
    """
    _temp = PageTemplateFile('answer_acknowledged.pt')
    if event.action in ('validate-answer-msa', ):
        observation = aq_parent(context)
        subject = 'Your answer was acknowledged'
        notify(observation, _temp, subject, ROLE_MSA, 'answer_acknowledged')
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/answer_to_msexperts.py
# Compiled at: 2019-05-21 05:08:42
from Acquisition import aq_parent
from esdrt.content.question import IQuestion
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IQuestion, IActionSucceededEvent)
def notification_mse(context, event):
    """
    To:     MSExperts
    When:   New question for your country
    """
    _temp = PageTemplateFile('answer_to_msexperts.pt')
    if event.action in ('phase1-assign-answerer', 'phase2-assign-answerer'):
        observation = aq_parent(context)
        subject = 'New question for your country'
        notify(observation, _temp, subject, 'MSExpert', 'answer_to_msexperts')
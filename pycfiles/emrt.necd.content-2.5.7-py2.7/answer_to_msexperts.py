# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/answer_to_msexperts.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_MSE

def notification_mse(context, event=None, reassign=False):
    """
    To:     MSExperts
    When:   New question for your country
    """
    _temp = PageTemplateFile('answer_to_msexperts.pt')
    should_run = event and event.action in ('assign-answerer', ) or reassign
    if should_run:
        observation = aq_parent(context)
        subject = 'New question for your country'
        notify(observation, _temp, subject, ROLE_MSE, 'answer_to_msexperts')
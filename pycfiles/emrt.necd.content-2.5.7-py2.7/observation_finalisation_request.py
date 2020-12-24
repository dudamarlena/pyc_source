# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/observation_finalisation_request.py
# Compiled at: 2019-02-15 13:51:23
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_LR

def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   Observation finalisation request
    """
    _temp = PageTemplateFile('observation_finalisation_request.pt')
    if event.action in ('finish-observation', ):
        observation = context
        subject = 'Observation finalisation request'
        notify(observation, _temp, subject, ROLE_LR, 'observation_finalisation_request')
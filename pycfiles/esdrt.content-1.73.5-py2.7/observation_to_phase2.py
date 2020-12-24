# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/observation_to_phase2.py
# Compiled at: 2019-05-21 05:08:42
from esdrt.content.observation import IObservation
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   Observation handed over to phase 2
    """
    _temp = PageTemplateFile('observation_to_phase2.pt')
    if event.action in ('phase1-send-to-team-2', ):
        observation = context
        subject = 'Observation handed over to phase 2'
        notify(observation, _temp, subject, 'LeadReviewer', 'observation_to_phase2')


@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_rev_ph2(context, event):
    """
    To:     ReviewerPhase2
    When:   Observation handed over to phase 2
    """
    _temp = PageTemplateFile('observation_to_phase2_rev_msg.pt')
    if event.action in ('phase1-send-to-team-2', ):
        observation = context
        subject = 'Observation handed over to phase 2'
        notify(observation, _temp, subject, 'ReviewerPhase2', 'observation_to_phase2')
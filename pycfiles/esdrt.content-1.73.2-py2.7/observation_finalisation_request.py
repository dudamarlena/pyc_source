# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/esdrt/content/notifications/observation_finalisation_request.py
# Compiled at: 2019-05-21 05:08:42
from esdrt.content.observation import IObservation
from five import grok
from Products.CMFCore.interfaces import IActionSucceededEvent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify

@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_qe(context, event):
    """
    To:     QualityExpert
    When:   Observation finalisation request
    """
    _temp = PageTemplateFile('observation_finalisation_request.pt')
    if event.action in ('phase1-request-close', ):
        observation = context
        subject = 'Observation finalisation request'
        notify(observation, _temp, subject, 'QualityExpert', 'observation_finalisation_request')


@grok.subscribe(IObservation, IActionSucceededEvent)
def notification_lr(context, event):
    """
    To:     LeadReviewer
    When:   Observation finalisation request
    """
    _temp = PageTemplateFile('observation_finalisation_request.pt')
    if event.action in ('phase2-finish-observation', ):
        observation = context
        subject = 'Observation finalisation request'
        notify(observation, _temp, subject, 'LeadReviewer', 'observation_finalisation_request')
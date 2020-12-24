# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/observation_finalised.py
# Compiled at: 2019-02-15 13:51:23
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_MSA
from emrt.necd.content.constants import ROLE_SE

def notification_ms(context, event):
    """
    To:     MSAuthority
    When:   Observation was finalised
    """
    _temp = PageTemplateFile('observation_finalised.pt')
    if event.action in ('confirm-finishing-observation', ):
        observation = context
        subject = 'An observation for your country was finalised'
        notify(observation, _temp, subject, ROLE_MSA, 'observation_finalised')


def notification_se(context, event):
    """
    To:     SectorExpert
    When:   Observation finalised
    """
    _temp = PageTemplateFile('observation_finalised_rev_msg.pt')
    if event.action in ('confirm-finishing-observation', ):
        observation = context
        subject = 'Your observation was finalised'
        notify(observation, _temp, subject, ROLE_SE, 'observation_finalised')
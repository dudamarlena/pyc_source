# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/emrt/necd/content/notifications/question_redraft.py
# Compiled at: 2019-02-15 13:51:23
from Acquisition import aq_parent
from Products.Five.browser.pagetemplatefile import PageTemplateFile
from utils import notify
from emrt.necd.content.constants import ROLE_SE

def notification_se(context, event):
    """
    To:     SectorExpert
    When:   Redraft requested by LR.
    """
    _temp = PageTemplateFile('question_redraft.pt')
    if event.action in ('redraft', ):
        observation = aq_parent(context)
        subject = 'Redraft requested.'
        notify(observation, _temp, subject, ROLE_SE, 'question_redraft')
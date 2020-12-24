# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\Products\PloneStatCounter\browser.py
# Compiled at: 2008-07-06 19:44:50
from zope.component import getUtility
from zope.formlib import form
from zope.i18nmessageid import MessageFactory
from Products.Five.formlib import formbase
from interfaces import IStatCounterConfig
_ = MessageFactory('Products.PloneStatCounter')

class StatCounterConfigForm(formbase.EditFormBase):
    __module__ = __name__
    form_fields = form.Fields(IStatCounterConfig)
    label = _('StatCounter configuration form')


def form_adapter(context):
    return getUtility(IStatCounterConfig, name='statcounter_config', context=context)
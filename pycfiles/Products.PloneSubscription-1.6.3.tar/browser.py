# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
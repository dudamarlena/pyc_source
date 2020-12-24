# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Products/BastionZenoss/monkeypatches.py
# Compiled at: 2011-01-11 16:22:56
import logging
from Acquisition import aq_inner
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
logger = logging.getLogger('BastionZenoss')

def noop(*args, **kw):
    pass


logger.info('monkeypatching ZenUtils.Security')
from Products.ZenUtils import Security
Security._createInitialUser = noop
from Products.ZenUI3.browser.macros import PageTemplateMacros, BBBMacros
PTMacros_get_orig = PageTemplateMacros.__getitem__

def PTMacros_get(self, key):
    if key in ('page1', 'page2'):
        return getattr(aq_inner(self.context), 'templates').macros[key]
    return PTMacros_get_orig(self, key)


def BBBMacros_get(self, key):
    if key == 'macros':
        return self
    return getattr(aq_inner(self.context), 'templates').macros[key]


logger.info('Monkeypatching main templates overrides')
PageTemplateMacros.__getitem__ = PTMacros_get
BBBMacros.__getitem__ = BBBMacros_get
from ZPublisher.Converters import type_converters, field2string
type_converters['password'] = field2string
logger.info('added type converter: password')
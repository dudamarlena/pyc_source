# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/baseskin/viewlet.py
# Compiled at: 2014-04-28 09:39:49
__docformat__ = 'restructuredtext'
from zope.contentprovider.interfaces import IContentProvider
from ztfy.baseskin.interfaces.form import IFormViewletsManager, IFormPrefixViewletsManager, IWidgetsPrefixViewletsManager, IWidgetsSuffixViewletsManager, IFormSuffixViewletsManager
from z3c.template.template import getViewTemplate
from zope.component import adapts
from zope.interface import implements, Interface
from zope.viewlet.viewlet import ViewletBase as Viewlet
from zope.viewlet.manager import ViewletManagerBase as ViewletManager, WeightOrderedViewletManager
from ztfy.baseskin.layer import IBaseSkinLayer

class ViewletManagerBase(ViewletManager):
    """Template based viewlet manager class"""
    template = getViewTemplate()


class WeightViewletManagerBase(WeightOrderedViewletManager):
    """Template based weighted viewlet manager class"""
    template = getViewTemplate()


class ViewletBase(Viewlet):
    """Template based viewlet"""
    render = getViewTemplate()


class ContentProviderBase(object):
    """Generic template based content provider"""
    adapts(Interface, IBaseSkinLayer, Interface)
    implements(IContentProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        pass

    render = getViewTemplate()


class FormViewletManager(WeightOrderedViewletManager):
    """Base form viewlet manager"""
    implements(IFormViewletsManager)


class FormPrefixViewletManager(FormViewletManager):
    """Form prefix viewlet manager, displayed before form"""
    implements(IFormPrefixViewletsManager)


class WidgetsPrefixViewletManager(FormViewletManager):
    """Form widgets prefix display manager, displayed before widgets"""
    implements(IWidgetsPrefixViewletsManager)


class WidgetsSuffixViewletManager(FormViewletManager):
    """Form widgets suffix viewlet manager, displayed after widgets"""
    implements(IWidgetsSuffixViewletsManager)


class FormSuffixViewletManager(FormViewletManager):
    """Form suffix viewlet manager, displayed after form"""
    implements(IFormSuffixViewletsManager)
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ice/control/browser/menu.py
# Compiled at: 2010-08-27 06:32:04
from zope.security import canAccess
from zope.interface import implements
from zope.component import getAdapters, getMultiAdapter
from zope.contentprovider.interfaces import IContentProvider
from zope.authentication.interfaces import IUnauthenticatedPrincipal
from z3c.template.interfaces import IContentTemplate
from interfaces import IControlPagelet

class Menu:
    implements(IContentProvider)

    def __init__(self, context, request, view):
        self.context = context
        self.request = request
        self.__parent__ = view

    def update(self):
        pagelets = getAdapters((self.context, self.request), IControlPagelet)
        self.pagelets = [ v for (k, v) in pagelets if canAccess(v, '__call__') ]
        self.pagelets.sort(key=lambda x: x.weight)

    def render(self):
        template = getMultiAdapter((self, self.request), IContentTemplate)
        return template(self)

    def noauth(self):
        return IUnauthenticatedPrincipal.providedBy(self.request.principal)
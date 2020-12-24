# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/adding.py
# Compiled at: 2006-12-07 13:02:03
"""shortcut adding

$Id: adding.py 1876 2005-05-31 22:23:43Z gary $
"""
from zope import interface, component
from zope.event import notify
import zope.security.checker
from zope.security.proxy import removeSecurityProxy
from zope.component.interfaces import IFactory
from zope.app.component.hooks import getSite
import zope.app.container.browser.adding
from zope.app.container.constraints import checkObject
from zope.lifecycleevent import ObjectCreatedEvent
from zope.exceptions.interfaces import UserError
from zope.location.interfaces import ILocation
from zope.location import LocationProxy
from zc.shortcut import Shortcut, traversedURL, interfaces

class Adding(zope.app.container.browser.adding.Adding):
    __module__ = __name__
    interface.implements(interfaces.IAdding)

    def action(self, type_name='', id=''):
        if not type_name:
            raise UserError(_('You must select the type of object to add.'))
        if type_name.startswith('@@'):
            type_name = type_name[2:]
        if '/' in type_name:
            view_name = type_name.split('/', 1)[0]
        else:
            view_name = type_name
        if component.queryMultiAdapter((self, self.request), name=view_name) is not None:
            url = '%s/@@+/%s=%s' % (traversedURL(self.context, self.request), type_name, id)
            self.request.response.redirect(url)
            return
        if not self.contentName:
            self.contentName = id
        factory = component.getUtility(IFactory, type_name)
        if type(factory) is not zope.security.checker.Proxy:
            factory = LocationProxy(factory, self, type_name)
            factory = zope.security.checker.ProxyFactory(factory)
        content = factory()
        content = removeSecurityProxy(content)
        notify(ObjectCreatedEvent(content))
        self.add(content)
        self.request.response.redirect(self.nextURL())
        return

    def nextURL(self):
        """See zope.app.container.interfaces.IAdding"""
        content = self.context[self.contentName]
        nextURL = component.queryMultiAdapter((self, content, self.context), name=interfaces.NEXT_URL_NAME)
        if nextURL is None:
            nextURL = traversedURL(self.context, self.request) + '/@@contents.html'
        return nextURL
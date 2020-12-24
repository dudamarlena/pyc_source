# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/zc/shortcut/factory.py
# Compiled at: 2006-12-07 13:02:03
from zope import interface, event, component
import zope.component.factory
from zope.app.container.interfaces import INameChooser, IContainer
from zope.app.container.constraints import checkObject
from zope.lifecycleevent import ObjectCreatedEvent
from zc.shortcut import interfaces, Shortcut

class Factory(zope.component.factory.Factory):
    __module__ = __name__
    interface.implements(interfaces.IShortcutFactory)

    def __init__(self, *args, **kw):
        shortcut_factory = kw.pop('shortcut_factory', None)
        if shortcut_factory is None:
            shortcut_factory = Shortcut
        self._shortcut_factory = shortcut_factory
        super(Factory, self).__init__(*args, **kw)
        return

    def __call__(self, *args, **kw):
        content = self._callable(*args, **kw)
        event.notify(ObjectCreatedEvent(content))
        repository = component.getAdapter(content, IContainer, interfaces.REPOSITORY_NAME)
        chooser = INameChooser(repository)
        name = chooser.chooseName('', content)
        checkObject(repository, name, content)
        repository[name] = content
        return self._shortcut_factory(repository[name])

    def getInterfaces(self):
        return interface.implementedBy(self._shortcut_factory)

    def getTargetInterfaces(self):
        return super(Factory, self).getInterfaces()
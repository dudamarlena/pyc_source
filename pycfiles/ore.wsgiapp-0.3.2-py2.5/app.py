# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/app.py
# Compiled at: 2008-05-01 10:27:18
from zope import interface
from zope.app.component import site
from zope.app.container.sample import SampleContainer
from zope.traversing.interfaces import IContainmentRoot
import interfaces

class BaseApplication(site.SiteManagerContainer):
    interface.implements(interfaces.IApplication, IContainmentRoot)


class Application(SampleContainer, BaseApplication):
    pass
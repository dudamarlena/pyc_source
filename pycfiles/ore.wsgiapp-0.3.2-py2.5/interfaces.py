# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/wsgiapp/interfaces.py
# Compiled at: 2008-05-01 10:27:18
"""
$Id: $
"""
from zope import interface
from zope.component.interfaces import IObjectEvent

class IApplication(interface.Interface):
    """
    Application Root to publish
    """
    pass


class IWSGIApplicationCreatedEvent(IObjectEvent):
    app = interface.Attribute('Published Application')


class WSGIApplicationCreatedEvent(object):
    interface.implements(IWSGIApplicationCreatedEvent)

    def __init__(self, object):
        self.object = object
# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/ore/viewlet/interfaces.py
# Compiled at: 2008-05-19 13:01:22
"""
$Id: interfaces.py 1962 2007-05-18 19:37:09Z hazmat $
"""
from zope.interface import Interface
from zope.viewlet import interfaces as viewapi
from zope.formlib.interfaces import IForm

class IEventManager(Interface):
    """ an object implementing a private event channel
    """

    def notify(event):
        """
        publish an event to contained viewlets
        """
        pass


class IEventViewlet(Interface):

    def notify(event):
        """
        receive an event on the private event channel 
        """
        pass


class IStorageManager(Interface):
    """ an providing persistent annotation access for values
    """

    def storage(name=None):
        """ return viewlet persistent mapping, if name specified its
        the mapping is namespaced
        """
        pass


class IFormViewlet(viewapi.IViewlet, IForm):
    """ a viewlet which utilizes formlib for forms or actions
    """
    pass


class IViewComponent(viewapi.IViewlet):
    """ a functional component viewlet with ajax interaction with the
    browser, component assets are directly addressable by url, they are
    not view themselves.
    """

    def show():
        """ should this view component be displayed on the current page
        """
        pass
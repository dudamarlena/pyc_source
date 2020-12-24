# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/pushpage/interfaces.py
# Compiled at: 2006-10-05 16:04:27
""" PushPage events

$Id: interfaces.py,v 1.1 2006/10/05 20:04:27 tseaver Exp $
"""
from zope.interface import Interface
from zope.interface import Attribute

class IPushPageEvent(Interface):
    """ Base for events related to publishing pushpage objects.
    """
    __module__ = __name__
    page = Attribute('Pushpage\n\n        The page about whom the event is published.')


class IPushPageNamespaceInit(IPushPageEvent):
    """ Event published after extracting the namespace from the callable.
    """
    __module__ = __name__
    namespace = Attribute('Namespace\n\n        A dict containing names returned from the callable.  Subscribers\n        may mutate at will.')


class IPushPageRendered(IPushPageEvent):
    """ Event published after rendering a pushpage.
    """
    __module__ = __name__
    rendered = Attribute('Rendered Text\n\n        The text rendered by the pushpage.')
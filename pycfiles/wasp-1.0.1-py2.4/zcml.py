# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/wasp/demo/zcml.py
# Compiled at: 2008-09-17 11:14:28
from wasp.demo import SendMessage
from wasp.interfaces import ISendMessage
from zope.component.zcml import utility
from zope.configuration.fields import Bool
from zope.interface import Interface

class ISenderDirective(Interface):
    """Setup a demo SendMessage utility."""
    __module__ = __name__
    response = Bool(title='Return value', description='Configures whether the SendMessage utility will return True or False when called', required=False)


def setupUtility(_context, response=None):
    kw = {}
    if response is not None:
        kw['response'] = response
    sender = SendMessage(**kw)
    utility(_context, ISendMessage, sender)
    return
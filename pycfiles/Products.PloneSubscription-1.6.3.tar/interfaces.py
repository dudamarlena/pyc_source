# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\Products\PloneStatCounter\interfaces.py
# Compiled at: 2008-07-07 15:09:40
from zope.interface import Interface
from zope import schema
from zope.i18nmessageid import MessageFactory
from zope.viewlet.interfaces import IViewlet
_ = MessageFactory('Products.PloneStatCounter')

class IStatCounterConfig(Interface):
    """Configuration for a StatCounter configlet.
    """
    __module__ = __name__
    sc_project = schema.TextLine(title=_('Project id'), required=True)
    sc_invisible = schema.Bool(title=_('Invisible counter?'), default=True)
    sc_partition = schema.TextLine(title=_('Partition'), required=True)
    sc_security = schema.TextLine(title=_('Security code'), required=True)


class IStatCounterViewlet(IViewlet):
    """
    """
    __module__ = __name__

    def renderJavascriptVariables(self):
        """Return rendered javascript variables for StatCounter.
        """
        pass
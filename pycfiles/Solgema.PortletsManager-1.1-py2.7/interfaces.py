# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/Solgema/PortletsManager/interfaces.py
# Compiled at: 2013-06-12 05:30:12
from zope.interface import Interface, Attribute
from plone.theme.interfaces import IDefaultPloneLayer
from zope.i18nmessageid import MessageFactory
from plone.portlets.interfaces import IPortletAssignment
from zope import schema
from config import _

class ISolgemaPortletsManagerLayer(IDefaultPloneLayer):
    """Solgema portlets manager layer"""
    pass


class ISolgemaPortletManagerRetriever(Interface):
    """marker"""
    pass


class IPersistentOptions(Interface):
    """marker"""
    pass


class ISolgemaPortletAssignment(IPortletAssignment):
    """store stopped URLS"""
    stopUrls = schema.List(title=_('stopUrls', default='Urls to stop'), required=False, default=[])
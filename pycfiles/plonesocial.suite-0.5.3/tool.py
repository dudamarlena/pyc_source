# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/gyst/plonesocial.buildout/src/plonesocial.network/plonesocial/network/tool.py
# Compiled at: 2012-08-14 05:15:05
from zope.interface import implements
from Products.CMFCore.utils import UniqueObject
from OFS.SimpleItem import SimpleItem
from interfaces import INetworkTool
from graph import NetworkGraph

class NetworkTool(UniqueObject, SimpleItem, NetworkGraph):
    """Provide INetworkContainer as a site utility."""
    implements(INetworkTool)
    meta_type = 'plonesocial.network tool'
    id = 'plonesocial_network'
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
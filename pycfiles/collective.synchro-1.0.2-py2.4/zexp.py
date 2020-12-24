# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/plugins/zexp.py
# Compiled at: 2008-12-16 18:21:19
"""
zexp pluggin adapter
"""
from random import random
import os
from collective.synchro.interfaces import IPluginExporter
from collective.synchro.interfaces import IZexpExporter
from collective.synchro.interfaces import IZexpImporter
from collective.synchro.data import ZexpPluginData
from zope.interface import implements
from App.config import getConfiguration

class ZexpExporter:
    """
    zexp plugin exporter
    """
    __module__ = __name__
    implements(IZexpExporter)

    def __init__(self, context):
        self.context = context

    def exportData(self):
        """
        export an IPlugginData
        """
        context = self.context
        zexpFile = context.getParentNode().manage_exportObject(id=context.getId(), download=True)
        return ZexpPluginData(zexpFile)


class ZexpImporter:
    __module__ = __name__
    implements(IZexpImporter)

    def __init__(self, data):
        self.data = data

    def importData(self, context):
        """
        import an IPluginData
        """
        filename = 'receivedZexp_%i.zexp' % (int(random() * 1000000),)
        cfg = getConfiguration()
        filepath = os.path.join(cfg.instancehome, 'import', filename)
        zfile = file(filepath, 'wb')
        zfile.write(self.data.getData())
        zfile.close()
        context.manage_importObject(filename)
        os.remove(filepath)
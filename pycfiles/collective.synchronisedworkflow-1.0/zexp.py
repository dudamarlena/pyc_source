# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/plugins/zexp.py
# Compiled at: 2008-12-16 18:21:19
__doc__ = '\nzexp pluggin adapter\n'
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
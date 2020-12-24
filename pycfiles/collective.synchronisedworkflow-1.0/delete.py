# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/plugins/delete.py
# Compiled at: 2008-12-16 18:21:19
__doc__ = ' delete event '
from zope.interface import implements
from collective.synchro.interfaces.plugin import IDeleteExporter
from collective.synchro.interfaces.plugin import IDeleteImporter
from collective.synchro.data import DeletePluginData
from collective.synchro import config

class PluginExporter(object):
    """
    unit class to export data
    """
    __module__ = __name__
    implements(IDeleteExporter)

    def __init__(self, context):
        self.context = context

    def exportData(self):
        """
        export an IPluginData
        """
        return DeletePluginData(self.context.getId())


class PluginImporter(object):
    __module__ = __name__
    implements(IDeleteImporter)

    def __init__(self, data):
        self.data = data

    def importData(self, context):
        """
        import an IPluginData
        """
        if self.data.getData() in context.objectIds():
            config.logger.info('delete %s in %s' % (self.data.getData(), ('/').join(context.getPhysicalPath())))
            context.manage_delObjects([self.data.getData()])
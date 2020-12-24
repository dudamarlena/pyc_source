# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/interfaces/tool.py
# Compiled at: 2008-12-16 18:21:20
from zope.interface import Interface
from Products.CMFPlone.interfaces import IPloneBaseTool

class ISynchronisationTool(IPloneBaseTool):
    __module__ = __name__

    def importContent(context):
        """ import data from file queue
            @param file:file name in queue
        """
        pass

    def exportContent(synchro_data, context):
        """ export data to file queue
            @param context:the context in queue
        """
        pass

    def registerPlugin(id, klass, priority, event):
        """ register an plugin for import export data
            @param id: identifier of plugin
                   klass: class name of the plugin
                   priority : priority of the plugin
                   event : interface of event on wich this plugin is registered
        """
        pass

    def unregisterPlugin(id):
        """ unregister plugin
            @param id: identifier of plugin
        """
        pass

    def getPlugins(event):
        """ return a list order by priority """
        pass
# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/datasources/DataSourceBase.py
# Compiled at: 2013-02-02 18:39:30
import urlparse
from Products.ZenModel.BasicDataSource import BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import Permissions
from Products.ZenUtils.Utils import binPath

class DataSourceBase(ZenPackPersistence, BasicDataSource):
    """
    A command-plugin that calls munin-based Zope-agents on remote
    instance via curl

    This base class needs instantiations with munin_plugins, and uri 
    attributes
    """
    ZOPE_MONITOR = 'ZopeMonitor'
    ZENPACKID = 'ZenPacks.lbn.ZopeMonitor'
    sourcetypes = (
     'COMMAND', ZOPE_MONITOR)
    sourcetype = 'COMMAND'
    eventClass = '/Status/Zope'
    zopeURI = '${here/zZopeURI}'
    timeout = 20
    parser = 'ZenPacks.lbn.ZopeMonitor.parsers.Munin'
    _properties = BasicDataSource._properties + ({'id': 'zopeURI', 'type': 'string', 'mode': 'w'}, {'id': 'timeout', 'type': 'int', 'mode': 'w'})
    _relations = BasicDataSource._relations + ()
    factory_type_information = (
     {'immediate_view': 'editZopeMonitorDataSource', 
        'actions': (
                  {'id': 'edit', 'name': 'Data Source', 
                     'action': 'editZopeMonitorDataSource', 
                     'permissions': (
                                   Permissions.view,)},)},)

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.__init__(self, id, title, buildRelations)

    def getDescription(self):
        """ DEBUGSTR """
        return '@@munin.zope.plugins/%s' % self.uri

    def useZenCommand(self):
        return True

    def getCommand(self, context):
        """ use curl to read munin.zope plugins on stdout """
        return BasicDataSource.getCommand(self, context, 'curl --max-time %i %s/@@munin.zope.plugins/%s' % (self.timeout, self.zopeURI, self.uri))

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        for tag in self.munin_tags:
            if not hasattr(self.datapoints, tag):
                self.manage_addRRDDataPoint(tag)

    def zmanage_editProperties(self, REQUEST=None):
        """validation, etc"""
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.zmanage_editProperties(self, REQUEST)
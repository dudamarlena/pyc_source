# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/oie/KannelMonitor/datasources/KannelDataSource.py
# Compiled at: 2012-01-12 17:51:59
import logging
from Products.ZenModel.BasicDataSource import BasicDataSource
from Products.ZenModel.ZenPackPersistence import ZenPackPersistence
from AccessControl import Permissions
from ZenPacks.oie.KannelMonitor.config import DATAPOINTS
LOG = logging.getLogger('KannelDataSource')

class KannelDataSource(ZenPackPersistence, BasicDataSource):
    """
    A command-plugin that calls the check_kannel nagios plugin to
    get input queue and throughput statistics from an SMPP bearer box.
    """
    KANNEL_MONITOR = 'KannelMonitor'
    ZENPACKID = 'ZenPacks.oie.KannelMonitor'
    sourcetypes = (
     KANNEL_MONITOR, 'COMMAND')
    sourcetype = 'COMMAND'
    eventClass = '/Status/Kannel'
    kannelServer = '${dev/id}'
    plugin = '${here/zKannelPlugin}'
    port = '${here/zKannelPort | string:13000}'
    secure = False
    password = ''
    timeout = 15
    parser = 'ZenPacks.oie.KannelMonitor.parsers.Kannel'
    _properties = BasicDataSource._properties + ({'id': 'timeout', 'type': 'int', 'mode': 'w'}, {'id': 'plugin', 'type': 'string', 'mode': 'w'}, {'id': 'secure', 'type': 'boolean', 'mode': 'w'}, {'id': 'password', 'type': 'string', 'mode': 'w'}, {'id': 'port', 'type': 'string', 'mode': 'w'})
    _relations = BasicDataSource._relations + ()
    factory_type_information = (
     {'immediate_view': 'editKannelMonitorDataSource', 
        'actions': (
                  {'id': 'edit', 'name': 'Data Source', 
                     'action': 'editKannelMonitorDataSource', 
                     'permissions': (
                                   Permissions.view,)},)},)

    def __init__(self, id, title=None, buildRelations=True):
        BasicDataSource.__init__(self, id, title, buildRelations)

    def getDescription(self):
        """ DEBUGSTR """
        if self.sourcetype == self.KANNEL_MONITOR:
            return self._cmd()
        return BasicDataSource.getDescription(self)

    def useZenCommand(self):
        return True

    def _cmd(self):
        cmd = self.plugin
        if self.timeout:
            cmd += ' --timeout=%s' % self.timeout
        if self.secure:
            cmd += ' --secure'
        if self.password:
            cmd += ' --password=%s' % self.password
        if self.port:
            cmd += ' --port=%s' % self.port
        return cmd

    def getCommand(self, context):
        """ use check_kannel to retrieve status info """
        return BasicDataSource.getCommand(self, context, self._cmd())

    def checkCommandPrefix(self, context, cmd):
        return cmd

    def addDataPoints(self):
        for tag in DATAPOINTS:
            if not hasattr(self.datapoints, tag):
                self.manage_addRRDDataPoint(tag)

    def zmanage_editProperties(self, REQUEST=None):
        """validation, etc"""
        if REQUEST:
            self.addDataPoints()
            if not REQUEST.form.get('eventClass', None):
                REQUEST.form['eventClass'] = self.__class__.eventClass
        return BasicDataSource.zmanage_editProperties(self, REQUEST)
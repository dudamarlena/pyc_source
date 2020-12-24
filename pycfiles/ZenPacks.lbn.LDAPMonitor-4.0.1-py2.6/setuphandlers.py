# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/setuphandlers.py
# Compiled at: 2012-01-17 21:23:24
from Acquisition import aq_base
from lbn.zenoss.packutils import addZenPackObjects
from Products.ZenEvents.EventClass import manage_addEventClass
from Products.ZenModel.RRDTemplate import manage_addRRDTemplate
from Products.ZenModel.MinMaxThreshold import MinMaxThreshold
from Products.ZenModel.DataPointGraphPoint import DataPointGraphPoint
import config
from datasources import LDAPDataSource

def setDataPoints(graphdef, tags):
    """
    control/tweak data point setup
    """
    pretty_names = map(lambda x: x[1], tags)
    graphdef.manage_addDataPointGraphPoints(pretty_names)
    for dp in graphdef.graphPoints():
        pretty_name = dp.getId()
        dp_name = filter(lambda x: x[1] == pretty_name, tags)[0][0]
        dp.dpName = 'ldap_%s' % dp_name


def install(zport, zenpack):
    """
    Set the collector plugin
    """
    dmd = zport.dmd
    if not getattr(aq_base(dmd.Events.Status), 'LDAP', None):
        manage_addEventClass(dmd.Events.Status, 'LDAP')
    collector = dmd.Monitors.Performance.localhost
    if not collector.hasProperty('perfldapCycleInterval'):
        collector.manage_addProperty('perfldapCycleInterval', 300, 'int')
    tpls = dmd.Devices.Server.rrdTemplates
    if getattr(aq_base(tpls), 'LDAPServer', None) is None:
        manage_addRRDTemplate(tpls, 'LDAPServer')
        tpl = tpls.LDAPServer
        tpl.manage_changeProperties(description='Monitors LDAP Servers', targetPythonClass='Products.ZenModel.Device')
        tpl.manage_addRRDDataSource('ldap', 'LDAPDataSource.LDAPDataSource')
        dst = tpl.datasources.ldap
        map(lambda x: dst.manage_addRRDDataPoint(x), map(lambda x: x[0], config.MONITORED) + ['responsetime'])
        map(lambda x: x.manage_changeProperties(rrdtype='DERIVE', rrdmin='0'), map(lambda x: dst.datapoints._getOb(x), map(lambda x: x[0], config.MONITORED)))
        gde = dst.manage_addGraphDefinition('Directory Server Errors')
        setDataPoints(gde, config.ERRORDP)
        gdb = dst.manage_addGraphDefinition('LDAP Binds')
        setDataPoints(gdb, config.BINDDP)
        gdo = dst.manage_addGraphDefinition('LDAP Operations')
        setDataPoints(gdo, config.OPSDP)
        gdc = dst.manage_addGraphDefinition('LDAP Performance')
        setDataPoints(gdc, config.CACHEDP)
        gdt = dst.manage_addGraphDefinition('LDAP Server Response Time')
        setDataPoints(gdt, (('responsetime', 'Response Time'), ))
        tpl.thresholds._setObject('BrokenLDAP', MinMaxThreshold('BrokenLDAP'))
        tpl.thresholds._getOb('BrokenLDAP').manage_changeProperties(DataPoints=['responsetime'], eventClass='/Status/LDAP', minval='300', maxval='30000', severity=5)
        tpl.thresholds._setObject('SlowLDAP', MinMaxThreshold('SlowLDAP'))
        tpl.thresholds._getOb('SlowLDAP').manage_changeProperties(DataPoints=['responsetime'], eventClass='/Status/LDAP', maxval='300', severity=3, escalateCount=6)
    pct = dmd.Monitors.rrdTemplates.PerformanceConf
    pct_gps = []
    if not getattr(pct.datasources, 'zenperfldap', None):
        perfds = pct.manage_addRRDDataSource('zenperfldap', 'BuiltInDS.Built-In')
        for (gdn, dpn, stacked, format) in (('Event Queue', 'eventQueueLength', True, '%6.0lf'),
         (
          'Data Point Rate', 'dataPoints', True, '%5.2lf%s'),
         (
          'Config Time', 'configTime', False, '%5.2lf%s'),
         (
          'Data Points', 'cyclePoints', False, '%5.2lf%s')):
            dp = perfds.manage_addRRDDataPoint(dpn)
            if dpn in ('dataPoints', ):
                dp.rrdtype = 'DERIVE'
                dp.rrdmin = 0
            gd = getattr(pct.graphDefs, gdn, None)
            if not gd:
                continue
            if hasattr(gd.graphPoints, 'zenperfldap'):
                continue
            gdp = gd.createGraphPoint(DataPointGraphPoint, 'zenperfldap')
            pct_gps.append(gdp)
            gdp.dpName = 'zenperfldap_%s' % dpn
            gdp.format = format
            gdp.stacked = stacked

    addZenPackObjects(zenpack, [zport.dmd.Events.Status.LDAP,
     tpls.LDAPServer,
     perfds] + pct_gps)
    return


def uninstall(zport):
    for (parent, id) in ((zport.dmd.Events.Status, 'Zope'),
     (
      zport.dmd.Devices.Server.rrdTemplates, 'ZopeServer')):
        if getattr(aq_base(parent), id, None):
            parent._delObject(id)

    collector = dmd.Monitors.Performance.localhost
    if collector.hasProperty('perfldapCycleInterval'):
        collector.manage_deleteProperties(('perfldapCycleInterval', ))
    return
# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/ZopeMonitor/setuphandlers.py
# Compiled at: 2013-01-08 08:48:09
import logging
from Acquisition import aq_base
from config import PROJECTNAME, MUNIN_THREADS, MUNIN_CACHE, MUNIN_ZODB, MUNIN_MEMORY
from lbn.zenoss.packutils import addZenPackObjects
from Products.ZenEvents.EventClass import manage_addEventClass
from Products.ZenModel.RRDTemplate import manage_addRRDTemplate
from datasources import ZopeThreadsDataSource, ZopeMemoryDataSource, ZopeCacheDataSource, ZopeDBActivityDataSource
logger = logging.getLogger(PROJECTNAME)
info = logger.info

def setDataPoints(graphdef, prefix, tags):
    pretty_tags = {}
    for tag in tags:
        if tag.find('_') != -1:
            pretty = tag.replace('_', ' ').capitalize()
        else:
            pretty = tag
        pretty_tags[pretty] = tag

    graphdef.manage_addDataPointGraphPoints(pretty_tags.keys())
    for dp in graphdef.graphPoints():
        dp.dpName = '%s_%s' % (prefix, pretty_tags[dp.getId()])

    info('added graph %s, datapoints(%s)' % (graphdef.getId(), (', ').join(pretty_tags.keys())))


def install(zport, zenpack):
    """
    Set the collector plugin
    """
    dmd = zport.dmd
    if not getattr(aq_base(dmd.Events.Status), 'Zope', None):
        manage_addEventClass(dmd.Events.Status, 'Zope')
    tpls = dmd.Devices.Server.rrdTemplates
    if getattr(aq_base(tpls), 'ZopeServer', None) is None:
        manage_addRRDTemplate(tpls, 'ZopeServer')
        tpl = tpls.ZopeServer
        tpl.manage_changeProperties(description='Monitors Zope Servers', targetPythonClass='Products.ZenModel.Device')
        tpl.manage_addRRDDataSource('zopethreads', 'ZopeThreadsDataSource.ZopeThreadsDataSource')
        tpl.manage_addRRDDataSource('zopecache', 'ZopeCacheDataSource.ZopeCacheDataSource')
        tpl.manage_addRRDDataSource('zodbactivity', 'ZopeDBActivityDataSource.ZopeDBActivitySource')
        tpl.manage_addRRDDataSource('zopememory', 'ZopeMemoryDataSource.ZopeMemoryDataSource')
        info('added DataSources: zopethreads, zopecache, zodbactivity, zopememory')
        dst = tpl.datasources.zopethreads
        map(lambda x: dst.manage_addRRDDataPoint(x), MUNIN_THREADS)
        gdt = dst.manage_addGraphDefinition('Zope Threads')
        setDataPoints(gdt, 'zopethreads', MUNIN_THREADS)
        dsc = tpl.datasources.zopecache
        map(lambda x: dsc.manage_addRRDDataPoint(x), MUNIN_CACHE)
        gdc = dsc.manage_addGraphDefinition('Zope Cache')
        setDataPoints(gdc, 'zopecache', MUNIN_CACHE)
        dsd = tpl.datasources.zodbactivity
        map(lambda x: dsd.manage_addRRDDataPoint(x), MUNIN_ZODB)
        gdd = dsd.manage_addGraphDefinition('ZODB Activity')
        setDataPoints(gdd, 'zodbactivity', MUNIN_ZODB)
        dsm = tpl.datasources.zopememory
        map(lambda x: dsm.manage_addRRDDataPoint(x), MUNIN_MEMORY)
        gdm = dsm.zopememory.manage_addGraphDefinition('Zope Memory')
        setDataPoints(gdm, 'zopememory', MUNIN_MEMORY)
    addZenPackObjects(zenpack, (zport.dmd.Events.Status.Zope, tpls.ZopeServer))
    return


def uninstall(zport):
    for (parent, id) in ((zport.dmd.Events.Status, 'Zope'),
     (
      zport.dmd.Devices.Server.rrdTemplates, 'ZopeServer')):
        if getattr(aq_base(parent), id, None):
            parent._delObject(id)

    return
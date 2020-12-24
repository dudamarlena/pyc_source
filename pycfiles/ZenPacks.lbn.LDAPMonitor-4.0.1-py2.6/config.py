# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/services/config.py
# Compiled at: 2012-01-12 19:19:26
import logging
from Products.ZenCollector.services.config import CollectorConfigService
from ZenPacks.lbn.LDAPMonitor.datasources.LDAPDataSource import LDAPDataSource
log = logging.getLogger('zen.ldapserviceconf')

class LDAPConfigService(CollectorConfigService):
    """
    place LDAP connection information into proxy
    """

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)
        proxy.configCycleInterval = self._prefs.perfsnmpCycleInterval
        proxy.datapoints = []
        proxy.thresholds = []
        log.debug('device: %s', device)
        try:
            perfServer = device.getPerformanceServer()
        except:
            return
        else:
            for comp in [device] + device.getMonitoredComponents():
                compName = comp.id
                try:
                    basepath = comp.rrdPath()
                except:
                    continue

                for templ in comp.getRRDTemplates():
                    dpnames = []
                    for ds in filter(lambda ds: isinstance(ds, LDAPDataSource), templ.getRRDDataSources()):
                        proxy.ldapuri = ds.ldapURI()
                        proxy.credentials = ds.ldapCredentials()
                        proxy.searchFilter = ds.searchFilter
                        for dp in ds.getRRDDataPoints():
                            dpname = dp.name()
                            dpnames.append(dpname)
                            proxy.datapoints.append((dp.id,
                             compName,
                             ('/').join((basepath, dpname)),
                             dp.rrdtype,
                             dp.getRRDCreateCommand(perfServer),
                             dp.rrdmin,
                             dp.rrdmax))

                    dpn = set(dpnames)
                    for thr in templ.thresholds():
                        if not (thr.enabled and dpn & set(thr.dsnames)):
                            continue
                        proxy.thresholds.append(thr.createThresholdInstance(comp))

        return proxy
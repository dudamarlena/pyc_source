# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/services/LDAPConfigService.py
# Compiled at: 2012-01-17 21:35:39
import logging
from Products.ZenCollector.services.config import CollectorConfigService
from ZenPacks.lbn.LDAPMonitor.datasources.LDAPDataSource import LDAPDataSource
log = logging.getLogger('zen.ldapserviceconf')

class LDAPConfigService(CollectorConfigService):
    """
    place LDAP connection information into proxy
    """

    def _filterDevice(self, device):
        """
        only return those with LDAP monitoring
        """
        return CollectorConfigService._filterDevice(self, device) and 'LDAPServer' in device.getProperty('zDeviceTemplates', [])

    def _createDeviceProxy(self, device):
        proxy = CollectorConfigService._createDeviceProxy(self, device)
        proxy.configCycleInterval = self._prefs.perfldapCycleInterval
        proxy.datapoints = []
        proxy.thresholds = []
        log.debug('device: %s', device)
        try:
            perfServer = device.getPerformanceServer()
        except:
            return
        else:
            compName = device.id
            basepath = device.rrdPath()
            for templ in device.getRRDTemplates():
                dpnames = []
                for ds in filter(lambda ds: isinstance(ds, LDAPDataSource), templ.getRRDDataSources()):
                    try:
                        proxy.ldapuri = ds.ldapURI(device)
                        proxy.credentials = (device.getProperty('zLDAPDN'), device.getProperty('zLDAPPW'))
                        proxy.searchFilter = ds.searchFilter
                    except:
                        log.error('Device not LDAP: %s' % device)
                        continue

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
                    proxy.thresholds.append(thr.createThresholdInstance(device))

        return proxy
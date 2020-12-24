# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ZenPacks/lbn/LDAPMonitor/zenperfldap.py
# Compiled at: 2012-03-27 23:02:06
import logging, ldap, time, pysamba.twisted.reactor
from zope.component import queryUtility
from zope.interface import implements
from twisted.internet import defer, reactor
from twisted.python.failure import Failure
from Products.ZenCollector.daemon import CollectorDaemon
from Products.ZenCollector.interfaces import ICollectorPreferences, IDataService, IEventService, IScheduledTask, IScheduledTaskFactory
from Products.ZenCollector.tasks import SimpleTaskFactory, SimpleTaskSplitter, TaskStates
from Products.ZenEvents.ZenEventClasses import Error, Clear, Critical
from Products.ZenUtils.observable import ObservableMixin
from Products.ZenUtils.Utils import unused
from Products.ZenCollector.services.config import DeviceProxy
unused(DeviceProxy)
import config
from monparsers import parse
log = logging.getLogger('zen.zenperfldap')
ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)

class ZenPerfLDAPPreferences(object):
    implements(ICollectorPreferences)

    def __init__(self):
        """
        Construct a new ZenPerfSqlPreferences instance and provide default
        values for needed attributes.
        """
        self.collectorName = 'zenperfldap'
        self.defaultRRDCreateCommand = None
        self.cycleInterval = 300
        self.configCycleInterval = 20
        self.options = None
        self.maxTasks = 1
        self.configurationService = 'ZenPacks.lbn.LDAPMonitor.services.LDAPConfigService'
        return

    def buildOptions(self, parser):
        parser.add_option('--debug', dest='debug', default=False, action='store_true', help='Increase logging verbosity.')
        parser.add_option('--sync', dest='sync', default=False, action='store_true', help='Force Synchronous query execution.')

    def postStartup(self):
        logseverity = self.options.logseverity


class ZenPerfLDAPTask(ObservableMixin):
    """
    gather ldap monitoring info and push it into rrd
    """
    implements(IScheduledTask)

    def __init__(self, taskName, deviceId, scheduleIntervalSeconds, taskConfig):
        """
        Construct a new task instance to get SQL data.

        @param deviceId: the Zenoss deviceId to watch
        @type deviceId: string
        @param taskName: the unique identifier for this task
        @type taskName: string
        @param scheduleIntervalSeconds: the interval at which this task will be
               collected
        @type scheduleIntervalSeconds: int
        @param taskConfig: the configuration for this task
        """
        super(ZenPerfLDAPTask, self).__init__()
        self.name = taskName
        self.configId = deviceId
        self.interval = scheduleIntervalSeconds
        self.state = TaskStates.STATE_IDLE
        self._taskConfig = taskConfig
        self._devId = deviceId
        self._manageIp = self._taskConfig.manageIp
        self._datapoints = self._taskConfig.datapoints
        self._thresholds = self._taskConfig.thresholds
        self._dataService = queryUtility(IDataService)
        self._eventService = queryUtility(IEventService)
        self._preferences = queryUtility(ICollectorPreferences, 'zenperfldap')

    def _failure(self, result, summary='Could not fetch statistics', severity=Error, comp=None):
        """
        Errback for an unsuccessful asynchronous connection or collection request.
        """
        err = result.getErrorMessage()
        log.error('Device %s: %s', self._devId, err)
        collectorName = self._preferences.collectorName
        self._eventService.sendEvent(dict(summary=summary, message=err, component=comp or collectorName, eventClass='/Status/LDAP', device=self._devId, severity=severity, agent=collectorName))
        return result

    def _sendEvents(self, components):
        """
        Send Error and Clear events 
        """
        events = []
        errors = []
        for (comp, severity) in components.iteritems():
            event = dict(summary='Could not fetch statistics', message='Could not fetch statistics', eventClass='/Status/LDAP', device=self._devId, severity=severity, agent=self._preferences.collectorName)
            if comp:
                event['component'] = comp
            if isinstance(severity, Failure):
                event['message'] = severity.getErrorMessage()
                event['severity'] = Error
                errors.append(event)
            else:
                events.append(event)

        if len(errors) == len(components) > 0:
            event = errors[0]
            del event['component']
            events.append(event)
        else:
            events.extend(errors)
        for event in events:
            self._eventService.sendEvent(event)

    def _collectSuccessful(self, results={}):
        """
        Callback for a successful fetch of monitor stats from the remote device.
        """
        log.debug('Successful collection from %s [%s], results=%s', self._devId, self._manageIp, results)
        compstatus = {}
        for (dpname, comp, rrdP, rrdT, rrdC, tmin, tmax) in self._datapoints:
            value = results.get(dpname, 0)
            compstatus[comp] = Clear
            try:
                self._dataService.writeRRD(rrdP, float(value), rrdT, rrdC, min=tmin, max=tmax)
            except Exception, e:
                compstatus[comp] = Failure(e)

        self._sendEvents(compstatus)
        return results

    def doTask(self):
        log.debug('Polling for stats from %s [%s]', self._devId, self._manageIp)
        ldapuri = self._taskConfig.ldapuri
        ldapcreds = self._taskConfig.credentials
        ldapfilter = self._taskConfig.searchFilter
        log.debug('%s %s %s' % (ldapuri, ldapcreds[0], ldapfilter))
        start_time = time.time()
        slapd = ldap.initialize(ldapuri)
        try:
            slapd.simple_bind_s(*ldapcreds)
        except ldap.INVALID_CREDENTIALS:
            msg = 'authentication failure: %s/%s: check credentials!' % (ldapuri, ldapcreds[0])
            return self._failure(Failure(ldap.LDAPError(msg)))
        except ldap.SERVER_DOWN:
            return self._failure(Failure(ldap.LDAPError('server uncontactable')), summary='LDAP server uncontactable', severity=Critical)
        except ldap.LDAPError, e:
            return self._failure(Failure(e))
        else:
            try:
                resultseq = slapd.search_s(ldapfilter, ldap.SCOPE_SUBTREE, attrlist=['*', '+'])
            except Exception, e:
                msg = 'search failure(%s): %s?%s: is cn=monitor activated?' % (str(e), ldapuri, ldapfilter)
                return self._failure(Failure(ldap.LDAPError(msg)))

        slapd.unbind()
        resp_time = time.time() - start_time
        results = parse(resultseq, {'responsetime': resp_time})
        self._collectSuccessful(results)

    def cleanup(self):
        pass


if __name__ == '__main__':
    myPreferences = ZenPerfLDAPPreferences()
    myTaskFactory = SimpleTaskFactory(ZenPerfLDAPTask)
    myTaskSplitter = SimpleTaskSplitter(myTaskFactory)
    daemon = CollectorDaemon(myPreferences, myTaskSplitter)
    daemon.run()
# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /web2ldap/app/metrics.py
# Compiled at: 2020-05-04 07:51:35
# Size of source mod 2**32: 4904 bytes
"""
web2ldap.app.metrics: Export several metrics with prometheus_client

web2ldap - a web-based LDAP Client,
see https://www.web2ldap.de for details

(c) 1998-2020 by Michael Stroeder <michael@stroeder.com>

This software is distributed under the terms of the
Apache License Version 2.0 (Apache-2.0)
https://www.apache.org/licenses/LICENSE-2.0
"""
import threading, web2ldap.__about__
from web2ldap.app.session import session_store, cleanUpThread
import web2ldap.app.gui, web2ldap.app.handler
from web2ldap.app.handler import COMMAND_COUNT
from ..ldapsession import LDAPSession
from ..log import logger, EXC_TYPE_COUNTER
try:
    import prometheus_client.core
except ImportError:
    METRICS_AVAIL = False
    logger.info('prometheus_client not installed => disable metrics!')
else:
    METRICS_AVAIL = True
if METRICS_AVAIL:
    from prometheus_client import REGISTRY
    from prometheus_client.metrics_core import CounterMetricFamily, GaugeMetricFamily
    from prometheus_client.openmetrics.exposition import generate_latest

    class MetricsCollector:
        __doc__ = '\n        Prometheus Python Client - Custom Collector\n\n        https://github.com/prometheus/client_python/blob/master/README.md#custom-collectors\n        '

        def _info(self):
            info = GaugeMetricFamily('web2ldap_info',
              'web2ldap installation information',
              labels=('version', 'major', 'minor', 'patchlevel'))
            info.add_metric((
             web2ldap.__about__.__version__,
             str(web2ldap.__about__.__version_info__.major),
             str(web2ldap.__about__.__version_info__.minor),
             str(web2ldap.__about__.__version_info__.micro)), 1)
            return info

        def _session_counters(self):
            sess_count = CounterMetricFamily('web2ldap_sessions',
              'Session counters',
              labels=('type', ))
            sess_count.add_metric(('all', ), session_store.sessionCounter)
            sess_count.add_metric(('removed', ), cleanUpThread.removed_sessions)
            return sess_count

        def _session_gauges(self):
            active_sessions_count = 0
            req_sessions_count = 0
            for k, i in session_store.sessiondict.items():
                if not k.startswith('__'):
                    if isinstance(i[1], LDAPSession):
                        if i[1].uri:
                            active_sessions_count += 1
                    req_sessions_count += 1
                sess_gauge = GaugeMetricFamily('web2ldap_sessions',
                  'Number of sessions',
                  labels=('type', ))
                sess_gauge.add_metric(('active', ), active_sessions_count)
                sess_gauge.add_metric(('limit', ), session_store.maxSessionCount)
                sess_gauge.add_metric(('req', ), req_sessions_count)
                sess_gauge.add_metric(('max', ), session_store.max_concurrent_sessions)
                return sess_gauge

        def _error_counts(self):
            excs = CounterMetricFamily('web2ldap_error',
              'Number of unhandled exceptions',
              labels=('type', ))
            for exc_class_name, exc_ctr in EXC_TYPE_COUNTER.items():
                excs.add_metric((exc_class_name,), exc_ctr)
            else:
                return excs

        def _cmd_counts(self):
            cmds = CounterMetricFamily('web2ldap_cmd',
              'Counters for command URLs',
              labels=('cmd', ))
            for cmd, cmd_ctr in COMMAND_COUNT.items():
                cmds.add_metric((cmd,), cmd_ctr)
            else:
                return cmds

        def collect(self):
            """
            yield all the metric instances
            """
            (yield self._info())
            (yield self._session_counters())
            (yield self._session_gauges())
            (yield self._error_counts())
            (yield self._cmd_counts())
            (yield GaugeMetricFamily('web2ldap_threads', 'Number of current threads', threading.activeCount()))


    METRICS_CONTENT_TYPE, METRICS_CHARSET = prometheus_client.CONTENT_TYPE_LATEST.split('; charset=')
    REGISTRY.register(MetricsCollector())

def w2l_metrics(app):
    """
    Send metrics to client
    """
    app.outf.set_headers(web2ldap.app.gui.gen_headers(content_type=METRICS_CONTENT_TYPE,
      charset=METRICS_CHARSET))
    app.outf.write_bytes(generate_latest(REGISTRY))
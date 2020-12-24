# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_ironic_inspector_log.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import ironic_inspector_log
from insights.tests import context_wrap
IRONIC_INSPECTOR_LOG = ("\n2019-03-01 03:53:02.814 4022 DEBUG futurist.periodics [-] Submitting periodic callback 'ironic_inspector.pxe_filter.base.periodic_sync_task' _process_scheduled /usr/lib/python2.7/site-packages/futurist/periodics.py:639\n2019-03-01 03:53:02.815 4022 DEBUG ironic_inspector.pxe_filter.base [-] The PXE filter driver DnsmasqFilter, state=initialized enters the fsm_reset_on_error context fsm_reset_on_error /usr/lib/python2.7/site-packages/ironic_inspector/pxe_filter/base.py:137\n2019-03-01 03:53:02.816 4022 DEBUG ironic_inspector.pxe_filter.dnsmasq [-] Syncing the driver _sync /usr/lib/python2.7/site-packages/ironic_inspector/pxe_filter/dnsmasq.py:79\n2019-03-01 03:53:02.881 4022 DEBUG ironic_inspector.pxe_filter.dnsmasq [-] The dnsmasq PXE filter was synchronized (took 0:00:00.065231) _sync /usr/lib/python2.7/site-packages/ironic_inspector/pxe_filter/dnsmasq.py:111\n2019-03-01 03:53:02.882 4022 DEBUG ironic_inspector.pxe_filter.base [-] The PXE filter driver DnsmasqFilter, state=initialized left the fsm_reset_on_error context fsm_reset_on_error /usr/lib/python2.7/site-packages/ironic_inspector/pxe_filter/base.py:153\n").strip()
IRONIC_INSPECTOR_ERROR_LOG = ("\n2018-12-05 17:20:41.404 25139 ERROR requests.packages.urllib3.connection [-] Certificate did not match expected hostname: 10.xx.xx.xx. Certificate: {'subjectAltName': (('DNS', '10.xx.xx.xx'),), 'notBefore': u'Dec  4 12:02:36 2018 GMT', 'serialNumber': u'616460101648CCDF5727C', 'notAfter': 'Jun 21 21:40:11 2019 GMT', 'version': 3L, 'subject': ((('commonName', u'10.xx.xx.xx'),),), 'issuer': ((('commonName', u'Local Signing Authority'),), (('commonName', u'616460a1-da41448c-cdf566ff'),))}\n").strip()

def test_ironic_inspector_log():
    log = ironic_inspector_log.IronicInspectorLog(context_wrap(IRONIC_INSPECTOR_LOG))
    assert len(log.lines) == 5


def test_ironic_inspector_error_log():
    log = ironic_inspector_log.IronicInspectorLog(context_wrap(IRONIC_INSPECTOR_ERROR_LOG))
    assert len(log.lines) == 1
    assert log.lines[0] == "2018-12-05 17:20:41.404 25139 ERROR requests.packages.urllib3.connection [-] Certificate did not match expected hostname: 10.xx.xx.xx. Certificate: {'subjectAltName': (('DNS', '10.xx.xx.xx'),), 'notBefore': u'Dec  4 12:02:36 2018 GMT', 'serialNumber': u'616460101648CCDF5727C', 'notAfter': 'Jun 21 21:40:11 2019 GMT', 'version': 3L, 'subject': ((('commonName', u'10.xx.xx.xx'),),), 'issuer': ((('commonName', u'Local Signing Authority'),), (('commonName', u'616460a1-da41448c-cdf566ff'),))}"


def test_ironic_inspector_log_documentation():
    failed_count, tests = doctest.testmod(ironic_inspector_log, globs={'log': ironic_inspector_log.IronicInspectorLog(context_wrap(IRONIC_INSPECTOR_ERROR_LOG))})
    assert failed_count == 0
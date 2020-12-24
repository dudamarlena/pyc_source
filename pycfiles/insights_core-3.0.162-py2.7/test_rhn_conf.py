# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_rhn_conf.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.rhn_conf import RHNConf
from insights.tests import context_wrap
RHN_TEST = ('\na=1\nb = 2\n\n#c = 3\nc = include an = sign\nserver.satellite.http_proxy = corporate_gateway.example.com:8080\nserver.satellite.http_proxy_username =\nserver.satellite.http_proxy_password =\n\ntraceback_mail = test@example.com, test@redhat.com\n\nweb.default_taskmaster_tasks = RHN::Task::SessionCleanup, RHN::Task::ErrataQueue,\n    RHN::Task::ErrataEngine,\n    RHN::Task::DailySummary, RHN::Task::SummaryPopulation,\n    RHN::Task::RHNProc,\n    RHN::Task::PackageCleanup\n\ndb_host =\nignored\n').strip()

def test_rhn_conf():
    r = RHNConf(context_wrap(RHN_TEST))
    assert r['a'] == '1'
    assert r['b'] == '2'
    assert r['c'] == 'include an = sign'
    assert r['server.satellite.http_proxy_username'] == ''
    assert r['traceback_mail'] == ['test@example.com', 'test@redhat.com']
    assert r['web.default_taskmaster_tasks'] == [
     'RHN::Task::SessionCleanup', 'RHN::Task::ErrataQueue',
     'RHN::Task::ErrataEngine', 'RHN::Task::DailySummary',
     'RHN::Task::SummaryPopulation', 'RHN::Task::RHNProc',
     'RHN::Task::PackageCleanup']
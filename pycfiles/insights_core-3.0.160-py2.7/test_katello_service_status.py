# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_katello_service_status.py
# Compiled at: 2019-05-16 13:41:33
from ...tests import context_wrap
from ..katello_service_status import KatelloServiceStatus
KS_OUT = '\npulp_celerybeat (pid 443) is running.\ncelery init v10.0.\nUsing config script: /etc/default/pulp_workers\nnode reserved_resource_worker-0 (pid 902) is running...\nnode reserved_resource_worker-1 (pid 921) is running...\nnode reserved_resource_worker-2 (pid 938) is running...\nnode reserved_resource_worker-3 (pid 959) is running...\ncelery init v10.0.\nUsing config script: /etc/default/pulp_resource_manager\nnode resource_manager (pid 691) is running...\ntomcat6 is stopped                                         [  OK  ]\ndynflow_executor is running.\ndynflow_executor_monitor is running.\nhttpd is stopped\nSome services failed to status: tomcat6,httpd\n'
KS_OUT_1 = '\nSome services failed to status: httpd\n'
KS_OUT_2 = '\nUsing config script: /etc/default/pulp_resource_manager\nnode resource_manager (pid 691) is running...\nhttpd (pid  16006) is running..\ntomcat6 (pid 15560) is running...                          [  OK  ]\nSuccess!\n'

def test_kss():
    kss = KatelloServiceStatus(context_wrap(KS_OUT))
    assert kss.failed_services == ['tomcat6', 'httpd']
    assert not kss.is_ok
    kss = KatelloServiceStatus(context_wrap(KS_OUT_1))
    assert kss.failed_services == ['httpd']
    assert not kss.is_ok
    kss = KatelloServiceStatus(context_wrap(KS_OUT_2))
    assert kss.failed_services == []
    assert kss.is_ok
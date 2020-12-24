# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/plugins/insights_heartbeat.py
# Compiled at: 2019-05-16 13:41:33
from insights import rule, make_fail
from insights.parsers.hostname import Hostname
ERROR_KEY = 'INSIGHTS_HEARTBEAT'
HEARTBEAT_UUID = '9cd6f607-6b28-44ef-8481-62b0e7773614'
HOST = 'insights-heartbeat-' + HEARTBEAT_UUID

@rule(Hostname)
def is_insights_heartbeat(hostname):
    hostname = hostname.hostname
    if hostname == HOST:
        return make_fail(ERROR_KEY)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_netconsole.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.sysconfig import NetconsoleSysconfig
from insights.tests import context_wrap
netconsole = ("\n# This is the configuration file for the netconsole service.  By starting\n# this service you allow a remote syslog daemon to record console output\n# from this system.\n\n# The local port number that the netconsole module will use\nLOCALPORT=6666\n\n# The ethernet device to send console messages out of (only set this if it\n# can't be automatically determined)\n# DEV=\n\n# The IP address of the remote syslog server to send messages to\n# SYSLOGADDR=\n\n# The listening port of the remote syslog daemon\nSYSLOGPORT=514\n\n# The MAC address of the remote syslog server (only set this if it can't\n# be automatically determined)\n# SYSLOGMACADDR=\n").strip()

def test_netconsole():
    result = NetconsoleSysconfig(context_wrap(netconsole))
    assert result['LOCALPORT'] == '6666'
    assert result.get('DEV') is None
    assert result['SYSLOGPORT'] == '514'
    return
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_vmware_tools_conf.py
# Compiled at: 2019-05-16 13:41:33
import doctest
from insights.parsers import vmware_tools_conf
from insights.tests import context_wrap
CONF = '\n[guestinfo]\ndisable-query-diskinfo = true\n\n[logging]\nlog = true\n\nvmtoolsd.level = debug\nvmtoolsd.handler = file\nvmtoolsd.data = /tmp/vmtoolsd.log\n'

def test_vmware_tools_conf():
    conf = vmware_tools_conf.VMwareToolsConf(context_wrap(CONF))
    assert list(conf.sections()) == ['guestinfo', 'logging']
    assert conf.has_option('guestinfo', 'disable-query-diskinfo') is True
    assert conf.getboolean('guestinfo', 'disable-query-diskinfo') is True
    assert conf.get('guestinfo', 'disable-query-diskinfo') == 'true'
    assert conf.get('logging', 'vmtoolsd.handler') == 'file'
    assert conf.get('logging', 'vmtoolsd.data') == '/tmp/vmtoolsd.log'


def test_vmware_tools_conf_documentation():
    failed_count, tests = doctest.testmod(vmware_tools_conf, globs={'conf': vmware_tools_conf.VMwareToolsConf(context_wrap(CONF))})
    assert failed_count == 0
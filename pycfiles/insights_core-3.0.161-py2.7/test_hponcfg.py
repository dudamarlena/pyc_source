# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_hponcfg.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.hponcfg import HponConf
from insights.tests import context_wrap
HPONCFG = '\nHP Lights-Out Online Configuration utility\nVersion 4.3.1 Date 05/02/2014 (c) Hewlett-Packard Company, 2014\nFirmware Revision = 1.40 Device type = iLO 4 Driver name = hpilo\nHost Information:\n                        Server Name: foo.example.com\n                        Server Number:\n'

def test_hponcfg():
    conf = HponConf(context_wrap(HPONCFG))
    assert '1.40' == conf.firmware_revision
    assert 'iLO 4' == conf.device_type
    assert 'hpilo' == conf.driver_name
    assert 'foo.example.com' == conf['server_name']
    assert '' == conf['server_number']
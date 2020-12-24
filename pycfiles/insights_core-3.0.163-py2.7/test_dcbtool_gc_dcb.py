# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dcbtool_gc_dcb.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import dcbtool_gc_dcb
from insights.tests import context_wrap
DCBTOOL_GC_OUTPUT = '\n\n    Command:    Get Config\n    Feature:    DCB State\n    Port:       eth0\n    Status:     Off\n    DCBX Version: FORCED CIN\n\n'
DCBTOOL_GC_DCB_FAILED = '\nconnect: Connection refused\nFailed to connect to lldpad - clif_open: Connection refused\n'

def test_dcbtool_gc():
    result = dcbtool_gc_dcb.Dcbtool(context_wrap(DCBTOOL_GC_OUTPUT))
    assert len(result.data) == 5
    assert result['command'] == 'Get Config'
    assert result['feature'] == 'DCB State'
    assert result['port'] == 'eth0'
    assert result['status'] == 'Off'
    assert result['dcbx_version'] == 'FORCED CIN'
    assert not result.is_on
    result = dcbtool_gc_dcb.Dcbtool(context_wrap(DCBTOOL_GC_DCB_FAILED))
    assert len(result.data) == 0
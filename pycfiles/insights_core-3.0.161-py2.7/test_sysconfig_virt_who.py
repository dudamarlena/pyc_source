# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_sysconfig_virt_who.py
# Compiled at: 2019-05-16 13:41:33
from insights.tests import context_wrap
from insights.parsers.sysconfig import VirtWhoSysconfig
VIRTWHO = ('\n# Register ESX machines using vCenter\n#VIRTWHO_ESX=0\n# Register guests using RHEV-M\n VIRTWHO_RHEVM=1\n\n# Options for RHEV-M mode\nVIRTWHO_RHEVM_OWNER=\n\nTEST_OPT="A TEST"\n').strip()

def test_sysconfig_virt_who():
    result = VirtWhoSysconfig(context_wrap(VIRTWHO))
    assert result['VIRTWHO_RHEVM'] == '1'
    assert result['VIRTWHO_RHEVM_OWNER'] == ''
    assert result.get('NO_SUCH_OPTIONS') is None
    assert 'NOSUCHOPTIONS' not in result
    assert result.get('TEST_OPT') == 'A TEST'
    return
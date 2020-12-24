# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_cciss.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers import cciss
from insights.tests import context_wrap
CCISS = '\ncciss0: HP Smart Array P220i Controller\nBoard ID: 0x3355103c\nFirmware Version: 3.42\nIRQ: 82\nLogical drives: 1\nSector size: 8192\nCurrent Q depth: 0\nCurrent # commands on controller: 0\nMax Q depth since init: 84\nMax # commands on controller since init: 111\nMax SG entries since init: 128\nSequential access devices: 0\n\ncciss/c0d0:  299.96GB   RAID 1(1+0)\n'

def test_get_cciss():
    cciss_info = cciss.Cciss(context_wrap(CCISS, path='/proc/devices/cciss0'))
    assert cciss_info.data['cciss0'] == 'HP Smart Array P220i Controller'
    assert cciss_info.data['Board ID'] == '0x3355103c'
    assert cciss_info.data['Firmware Version'] == '3.42'
    assert cciss_info.data['IRQ'] == '82'
    assert cciss_info.data['Logical drives'] == '1'
    assert cciss_info.data['Sector size'] == '8192'
    assert cciss_info.data['Current Q depth'] == '0'
    assert cciss_info.data['Current # commands on controller'] == '0'
    assert cciss_info.data['Max Q depth since init'] == '84'
    assert cciss_info.data['Max # commands on controller since init'] == '111'
    assert cciss_info.data['Max SG entries since init'] == '128'
    assert cciss_info.data['Sequential access devices'] == '0'
    assert cciss_info.data['cciss/c0d0'] == '299.96GB   RAID 1(1+0)'
    assert cciss_info.firmware_version == '3.42'
    assert cciss_info.model == 'HP Smart Array P220i Controller'
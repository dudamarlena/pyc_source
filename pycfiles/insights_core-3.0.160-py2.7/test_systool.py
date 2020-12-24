# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_systool.py
# Compiled at: 2019-05-16 13:41:33
import pytest
from insights.parsers.systool import SystoolSCSIBus, ParseException
from insights.tests import context_wrap
SYSTOOL_B_SCSI_V_1 = '\nBus = "scsi"\n\n  Device = "1:0:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1/target1:0:0/1:0:0:0"\n    delete              = <store method only>\n    device_blocked      = "0"\n    device_busy         = "0"\n    dh_state            = "detached"\n    eh_timeout          = "10"\n    evt_capacity_change_reported= "0"\n    evt_inquiry_change_reported= "0"\n    evt_lun_change_reported= "0"\n    evt_media_change    = "0"\n    evt_mode_parameter_change_reported= "0"\n    evt_soft_threshold_reached= "0"\n    iocounterbits       = "32"\n    iodone_cnt          = "0x15b"\n    ioerr_cnt           = "0x3"\n    iorequest_cnt       = "0x16c"\n    modalias            = "scsi:t-0x05"\n    model               = "CD-ROM          "\n    queue_depth         = "1"\n    queue_type          = "none"\n    rescan              = <store method only>\n    rev                 = "1.0 "\n    scsi_level          = "6"\n    state               = "running"\n    timeout             = "30"\n    type                = "5"\n    uevent              = "DEVTYPE=scsi_device\nDRIVER=sr\nMODALIAS=scsi:t-0x05"\n    unpriv_sgio         = "0"\n    vendor              = "VBOX    "\n\n  Device = "2:0:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:0d.0/ata3/host2/target2:0:0/2:0:0:0"\n    delete              = <store method only>\n    device_blocked      = "0"\n    device_busy         = "0"\n    dh_state            = "detached"\n    eh_timeout          = "10"\n    evt_capacity_change_reported= "0"\n    evt_inquiry_change_reported= "0"\n    evt_lun_change_reported= "0"\n    evt_media_change    = "0"\n    evt_mode_parameter_change_reported= "0"\n    evt_soft_threshold_reached= "0"\n    iocounterbits       = "32"\n    iodone_cnt          = "0x208c"\n    ioerr_cnt           = "0x2"\n    iorequest_cnt       = "0x20a6"\n    modalias            = "scsi:t-0x00"\n    model               = "VBOX HARDDISK   "\n    queue_depth         = "31"\n    queue_ramp_up_period= "120000"\n    queue_type          = "simple"\n    rescan              = <store method only>\n    rev                 = "1.0 "\n    scsi_level          = "6"\n    state               = "running"\n    timeout             = "30"\n    type                = "0"\n    uevent              = "DEVTYPE=scsi_device\nDRIVER=sd\nMODALIAS=scsi:t-0x00"\n    unpriv_sgio         = "0"\n    vendor              = "ATA     "\n    vpd_pg80            =\n    vpd_pg83            =\n\n  Device = "host0"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata1/host0"\n    uevent              = "DEVTYPE=scsi_host"\n\n  Device = "host1"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1"\n    uevent              = "DEVTYPE=scsi_host"\n\n  Device = "host2"\n  Device path = "/sys/devices/pci0000:00/0000:00:0d.0/ata3/host2"\n    uevent              = "DEVTYPE=scsi_host"\n\n  Device = "target1:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1/target1:0:0"\n    uevent              = "DEVTYPE=scsi_target"\n\n  Device = "target2:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:0d.0/ata3/host2/target2:0:0"\n    uevent              = "DEVTYPE=scsi_target"\n\n'
SYSTOOL_B_SCSI_V_ILLEGAL_2 = '\nBus = "scsi"\n\n  Device = "1:0:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1/target1:0:0/1:0:0:0"\n    delete              = <store method only>\n    type                is "5"\n    uevent              = "DEVTYPE=scsi_device\nDRIVER=sr\nMODALIAS=scsi:t-0x05"\n    unpriv_sgio         = "0"\n    vendor              = "VBOX    "\n'
SYSTOOL_B_SCSI_V_ILLEGAL_3 = '\nBus = "scsi"\n\n  Device = "1:0:0:0"\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1/target1:0:0/1:0:0:0"\n    delete              = <store method only>\n                        = "5"\n    uevent              = "DEVTYPE=scsi_device\nDRIVER=sr\nMODALIAS=scsi:t-0x05"\n    unpriv_sgio         = "0"\n    vendor              = "VBOX    "\n'
SYSTOOL_B_SCSI_V_ILLEGAL_4 = '\nBus = "scsi"\n\n  Device path = "/sys/devices/pci0000:00/0000:00:01.1/ata2/host1/target1:0:0/1:0:0:0"\n    delete              = <store method only>\n    type                = "5"\n    uevent              = "DEVTYPE=scsi_device\nDRIVER=sr\nMODALIAS=scsi:t-0x05"\n    unpriv_sgio         = "0"\n    vendor              = "VBOX    "\n'
SYSTOOL_B_SCSI_V_ILLEGAL_5 = '\nBus = "scsi"\n\n'
SYSTOOL_B_SCSI_V_ILLEGAL_6 = '\nBus = "abc"\n\n'

def test_systoolscsibus_with_legal_input():
    res = SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_1))
    assert len(res.data) == 7
    assert len(res.devices[0]) == 30
    assert len(res.devices[1]) == 33
    assert res.data['1:0:0:0']['uevent'] == 'DEVTYPE=scsi_device DRIVER=sr MODALIAS=scsi:t-0x05'
    assert res.data['1:0:0:0']['delete'] == '<store method only>'
    assert res.devices[1].get('vpd_pg83') == ''
    assert res.devices[1].get('not_exist') is None
    assert all([ d.get('Device path') for d in res.devices ])
    assert res.get_device_state('2:0:0:0') == 'running'
    assert res.get_device_state('host2') is None
    assert res.get_device_state('host_what') is None
    return


def test_systoolscsibus_with_illegal_input():
    with pytest.raises(ParseException) as (e_info):
        SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_ILLEGAL_2))
    assert 'Unparseable line without = ' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_ILLEGAL_3))
    assert 'Unparseable line without key' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_ILLEGAL_4))
    assert 'Parsing Error for no heading Device-name' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_ILLEGAL_5))
    assert 'Parsing Error for this almost empty input.' in str(e_info.value)
    with pytest.raises(ParseException) as (e_info):
        SystoolSCSIBus(context_wrap(SYSTOOL_B_SCSI_V_ILLEGAL_6))
    assert 'Unparseable first line of input:' in str(e_info.value)
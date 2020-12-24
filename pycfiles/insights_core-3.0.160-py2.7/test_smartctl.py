# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_smartctl.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.smartctl import SMARTctl
from insights.parsers import ParseException
from insights.tests import context_wrap
import pytest
STANDARD_DRIVE = '\nsmartctl 6.2 2013-07-26 r3841 [x86_64-linux-3.10.0-267.el7.x86_64] (local build)\nCopyright (C) 2002-13, Bruce Allen, Christian Franke, www.smartmontools.org\n\n=== START OF INFORMATION SECTION ===\nDevice Model:     ST500LM021-1KJ152\nSerial Number:    W620AT02\nLU WWN Device Id: 5 000c50 07817bb36\nFirmware Version: 0002LIM1\nUser Capacity:    500,107,862,016 bytes [500 GB]\nSector Sizes:     512 bytes logical, 4096 bytes physical\nRotation Rate:    7200 rpm\nDevice is:        Not in smartctl database [for details use: -P showall]\nATA Version is:   ATA8-ACS T13/1699-D revision 4\nSATA Version is:  SATA 3.0, 6.0 Gb/s (current: 6.0 Gb/s)\nLocal Time is:    Fri Sep 16 14:10:10 2016 AEST\nSMART support is: Available - device has SMART capability.\nSMART support is: Enabled\n\n=== START OF READ SMART DATA SECTION ===\nSMART overall-health self-assessment test result: PASSED\n\nGeneral SMART Values:\nOffline data collection status:  (0x00) Offline data collection activity\n                    was never started.\n                    Auto Offline Data Collection: Disabled.\nSelf-test execution status:      (   0) The previous self-test routine completed\n                    without error or no self-test has ever\n                    been run.\nTotal time to complete Offline\ndata collection:        (    0) seconds.\nOffline data collection\ncapabilities:            (0x73) SMART execute Offline immediate.\n                    Auto Offline data collection on/off support.\n                    Suspend Offline collection upon new\n                    command.\n                    No Offline surface scan supported.\n                    Self-test supported.\n                    Conveyance Self-test supported.\n                    Selective Self-test supported.\nSMART capabilities:            (0x0003) Saves SMART data before entering\n                    power-saving mode.\n                    Supports SMART auto save timer.\nError logging capability:        (0x01) Error logging supported.\n                    General Purpose Logging supported.\nShort self-test routine\nrecommended polling time:    (   1) minutes.\nExtended self-test routine\nrecommended polling time:    (  78) minutes.\nConveyance self-test routine\nrecommended polling time:    (   2) minutes.\nSCT capabilities:          (0x1031) SCT Status supported.\n                    SCT Feature Control supported.\n                    SCT Data Table supported.\n\nSMART Attributes Data Structure revision number: 10\nVendor Specific SMART Attributes with Thresholds:\nID# ATTRIBUTE_NAME          FLAG     VALUE WORST THRESH TYPE      UPDATED  WHEN_FAILED RAW_VALUE\n  1 Raw_Read_Error_Rate     0x000f   118   099   034    Pre-fail  Always       -       179599704\n  3 Spin_Up_Time            0x0003   098   098   000    Pre-fail  Always       -       0\n  4 Start_Stop_Count        0x0032   100   100   020    Old_age   Always       -       546\n  5 Reallocated_Sector_Ct   0x0033   100   100   036    Pre-fail  Always       -       0\n  7 Seek_Error_Rate         0x000f   078   060   030    Pre-fail  Always       -       61310462\n  9 Power_On_Hours          0x0032   096   096   000    Old_age   Always       -       4273 (5 89 0)\n 10 Spin_Retry_Count        0x0013   100   100   097    Pre-fail  Always       -       0\n 12 Power_Cycle_Count       0x0032   100   100   020    Old_age   Always       -       542\n184 End-to-End_Error        0x0032   100   100   099    Old_age   Always       -       0\n187 Reported_Uncorrect      0x0032   100   100   000    Old_age   Always       -       0\n188 Command_Timeout         0x0032   100   099   000    Old_age   Always       -       1\n189 High_Fly_Writes         0x003a   100   100   000    Old_age   Always       -       0\n190 Airflow_Temperature_Cel 0x0022   059   050   045    Old_age   Always       -       41 (Min/Max 21/41)\n191 G-Sense_Error_Rate      0x0032   100   100   000    Old_age   Always       -       19\n192 Power-Off_Retract_Count 0x0032   100   100   000    Old_age   Always       -       8\n193 Load_Cycle_Count        0x0032   099   099   000    Old_age   Always       -       3009\n194 Temperature_Celsius     0x0022   041   050   000    Old_age   Always       -       41 (0 11 0 0 0)\n196 Reallocated_Event_Count 0x000f   096   096   030    Pre-fail  Always       -       4258 (30941 0)\n197 Current_Pending_Sector  0x0012   100   100   000    Old_age   Always       -       0\n198 Offline_Uncorrectable   0x0010   100   100   000    Old_age   Offline      -       0\n199 UDMA_CRC_Error_Count    0x003e   200   200   000    Old_age   Always       -       0\n254 Free_Fall_Sensor        0x0032   100   100   000    Old_age   Always       -       0\n\nSMART Error Log Version: 1\nNo Errors Logged\n\nSMART Self-test log structure revision number 1\nNum  Test_Description    Status                  Remaining  LifeTime(hours)  LBA_of_first_error\n# 1  Short offline       Completed without error       00%      2315         -\n\nSMART Selective self-test log data structure revision number 1\n SPAN  MIN_LBA  MAX_LBA  CURRENT_TEST_STATUS\n    1        0        0  Not_testing\n    2        0        0  Not_testing\n    3        0        0  Not_testing\n    4        0        0  Not_testing\n    5        0        0  Not_testing\nSelective self-test flags (0x0):\n  After scanning selected spans, do NOT read-scan remainder of disk.\nIf Selective self-test is pending on power-up, resume after 0 minute delay.\n\n'

def test_standard_drive():
    data = SMARTctl(context_wrap(STANDARD_DRIVE, path='sos_commands/ata/smartctl_-a_.dev.sda'))
    assert data.device == '/dev/sda'
    assert data.information['Device Model'] == 'ST500LM021-1KJ152'
    assert data.information['Serial Number'] == 'W620AT02'
    assert data.information['LU WWN Device Id'] == '5 000c50 07817bb36'
    assert data.information['Firmware Version'] == '0002LIM1'
    assert data.information['User Capacity'] == '500,107,862,016 bytes [500 GB]'
    assert data.information['Sector Sizes'] == '512 bytes logical, 4096 bytes physical'
    assert data.information['Rotation Rate'] == '7200 rpm'
    assert data.information['Device is'] == 'Not in smartctl database [for details use: -P showall]'
    assert data.information['ATA Version is'] == 'ATA8-ACS T13/1699-D revision 4'
    assert data.information['SATA Version is'] == 'SATA 3.0, 6.0 Gb/s (current: 6.0 Gb/s)'
    assert data.information['Local Time is'] == 'Fri Sep 16 14:10:10 2016 AEST'
    assert data.information['SMART support is'] == 'Enabled'
    assert data.health == 'PASSED'
    assert data.values['Offline data collection status'] == '0x00'
    assert data.values['Self-test execution status'] == '0'
    assert data.values['Total time to complete Offline data collection'] == '0'
    assert data.values['Offline data collection capabilities'] == '0x73'
    assert data.values['SMART capabilities'] == '0x0003'
    assert data.values['Error logging capability'] == '0x01'
    assert data.values['Short self-test routine recommended polling time'] == '1'
    assert data.values['Extended self-test routine recommended polling time'] == '78'
    assert data.values['Conveyance self-test routine recommended polling time'] == '2'
    assert data.values['SCT capabilities'] == '0x1031'
    assert data.values['SMART Attributes Data Structure revision number'] == '10'
    assert data.attributes['Raw_Read_Error_Rate']['id'] == '1'
    assert data.attributes['Raw_Read_Error_Rate']['flag'] == '0x000f'
    assert data.attributes['Raw_Read_Error_Rate']['value'] == '118'
    assert data.attributes['Raw_Read_Error_Rate']['worst'] == '099'
    assert data.attributes['Raw_Read_Error_Rate']['threshold'] == '034'
    assert data.attributes['Raw_Read_Error_Rate']['type'] == 'Pre-fail'
    assert data.attributes['Raw_Read_Error_Rate']['updated'] == 'Always'
    assert data.attributes['Raw_Read_Error_Rate']['when_failed'] == '-'
    assert data.attributes['Raw_Read_Error_Rate']['raw_value'] == '179599704'
    assert data.attributes['Start_Stop_Count']['type'] == 'Old_age'
    assert data.attributes['Power_On_Hours']['raw_value'] == '4273 (5 89 0)'
    assert data.attributes['Airflow_Temperature_Cel']['raw_value'] == '41 (Min/Max 21/41)'
    assert data.attributes['Offline_Uncorrectable']['updated'] == 'Offline'
    assert not hasattr(data, 'full_line')
    assert not hasattr(data, 'info')


def test_bad_device():
    with pytest.raises(ParseException) as (exc):
        assert SMARTctl(context_wrap(STANDARD_DRIVE, path='sos_commands/ata/smartctl_-a')) is None
    assert 'Cannot parse device name from path ' in str(exc)
    return


CISCO_DRIVE = '\nsmartctl 5.43 2012-06-30 r3573 [x86_64-linux-2.6.32-573.8.1.el6.x86_64] (local build)\nCopyright (C) 2002-12 by Bruce Allen, http://smartmontools.sourceforge.net\n\nVendor:               Cisco\nProduct:              UCSC-MRAID12G\nRevision:             4.27\nUser Capacity:        898,999,779,328 bytes [898 GB]\nLogical block size:   512 bytes\nLogical Unit id:      0x678da6e715b756401d552c0c04e4953b\nSerial number:        003b95e4040c2c551d4056b715e7a68d\nDevice type:          disk\nLocal Time is:        Wed Dec 16 21:29:59 2015 EST\nDevice does not support SMART\n\nError Counter logging not supported\nDevice does not support Self Test logging\n'

def test_cisco_drive():
    data = SMARTctl(context_wrap(CISCO_DRIVE, path='sos_commands/ata/smartctl_-a_.dev.sdb'))
    assert data.device == '/dev/sdb'
    assert data.information['Vendor'] == 'Cisco'
    assert data.information['Product'] == 'UCSC-MRAID12G'
    assert data.information['Revision'] == '4.27'
    assert data.information['User Capacity'] == '898,999,779,328 bytes [898 GB]'
    assert data.information['Logical block size'] == '512 bytes'
    assert data.information['Logical Unit id'] == '0x678da6e715b756401d552c0c04e4953b'
    assert data.information['Serial number'] == '003b95e4040c2c551d4056b715e7a68d'
    assert data.information['Device type'] == 'disk'
    assert data.information['Local Time is'] == 'Wed Dec 16 21:29:59 2015 EST'
    assert data.information['SMART support is'] == 'Not supported'
    assert data.information['Error Counter logging'] == 'Not supported'
    assert data.information['Self Test logging'] == 'Not supported'
    assert data.health == 'not parsed'
    assert data.values == {}
    assert data.attributes == {}


NETAPP_DRIVE = '\nsmartctl 5.43 2012-06-30 r3573 [x86_64-linux-2.6.32-573.8.1.el6.x86_64] (local build)\nCopyright (C) 2002-12 by Bruce Allen, http://smartmontools.sourceforge.net\n\nVendor:               NETAPP\nProduct:              LUN\nRevision:             820a\nUser Capacity:        5,243,081,326,592 bytes [5.24 TB]\nLogical block size:   512 bytes\nLogical Unit id:      0x60a9800044312d364d5d4478753370620x5d447875337062000a980044312d364d\nSerial number:        D1-6M]Dxu3pb\nDevice type:          disk\nTransport protocol:   iSCSI\nLocal Time is:        Wed Dec 16 21:29:59 2015 EST\nDevice supports SMART and is Enabled\nTemperature Warning Disabled or Not Supported\nSMART Health Status: OK\n\nError Counter logging not supported\nDevice does not support Self Test logging\n\n'

def test_netapp_drive():
    data = SMARTctl(context_wrap(NETAPP_DRIVE, path='sos_commands/ata/smartctl_-a_.dev.sdc'))
    assert data.device == '/dev/sdc'
    assert data.information['Vendor'] == 'NETAPP'
    assert data.information['Product'] == 'LUN'
    assert data.information['Revision'] == '820a'
    assert data.information['User Capacity'] == '5,243,081,326,592 bytes [5.24 TB]'
    assert data.information['Logical block size'] == '512 bytes'
    assert data.information['Logical Unit id'] == '0x60a9800044312d364d5d4478753370620x5d447875337062000a980044312d364d'
    assert data.information['Serial number'] == 'D1-6M]Dxu3pb'
    assert data.information['Device type'] == 'disk'
    assert data.information['Transport protocol'] == 'iSCSI'
    assert data.information['Local Time is'] == 'Wed Dec 16 21:29:59 2015 EST'
    assert data.information['SMART Health Status'] == 'OK'
    assert data.information['SMART support is'] == 'Enabled'
    assert data.information['Temperature Warning'] == 'Disabled or Not Supported'
    assert data.information['Error Counter logging'] == 'Not supported'
    assert data.information['Self Test logging'] == 'Not supported'
    assert data.health == 'not parsed'
    assert data.values == {}
    assert data.attributes == {}
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/tests/test_dmidecode.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.dmidecode import DMIDecode
from insights.tests import context_wrap
from datetime import date
DMIDECODE = '\n# dmidecode 2.11\nSMBIOS 2.7 present.\n188 structures occupying 5463 bytes.\nTable at 0xBFFCB000.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: HP\n\tVersion: P70\n\tRelease Date: 03/01/2013\n\tAddress: 0xF0000\n\tRuntime Size: 64 kB\n\tROM Size: 8192 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tPNP is supported\n\t\tBIOS is upgradeable\n\t\tBIOS shadowing is allowed\n\t\tESCD support is available\n\t\tBoot from CD is supported\n\t\tSelectable boot is supported\n\t\tEDD is supported\n\t\t5.25"/360 kB floppy services are supported (int 13h)\n\t\t5.25"/1.2 MB floppy services are supported (int 13h)\n\t\t3.5"/720 kB floppy services are supported (int 13h)\n\t\tPrint screen service is supported (int 5h)\n\t\tj042 keyboard services are supported (int 9h)\n\t\tSerial services are supported (int 14h)\n\t\tPrinter services are supported (int 17h)\n\t\tCGA/mono video services are supported (int 10h)\n\t\tACPI is supported\n\t\tUSB legacy is supported\n\t\tBIOS boot specification is supported\n\t\tFunction key-initiated network boot is supported\n\t\tTargeted content distribution is supported\n\tFirmware Revision: 1.22\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: HP\n\tProduct Name: ProLiant DL380p Gen8\n\tVersion: Not Specified\n\tSerial Number: 2M23360006\n\tUUID: 34373936-3439-4D32-3233-333630303036\n\tWake-up Type: Power Switch\n\tSKU Number: 697494-S01\n\tFamily: ProLiant\n\nHandle 0x0300, DMI type 3, 21 bytes\nchassis information\n\tmanufacturer: hp\n\ttype: rack mount chassis\n\tlock: not present\n\tversion: not specified\n\tserial number: 2m23360006\n\tasset Tag:\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n\tOEM Information: 0x00000000\n\tHeight: 2 U\n\tNumber Of Power Cords: 2\n\tContained Elements: 0\n\nHandle 0x0401, DMI type 4, 32 bytes\nProcessor Information\n\tSocket Designation: CPU 1\n\tType: Central Processor\n\tFamily: Other\n\tManufacturer: Bochs\n\tID: A1 06 02 00 FD FB 8B 17\n\tVersion: Not Specified\n\tVoltage: Unknown\n\tExternal Clock: Unknown\n\tMax Speed: 2000 MHz\n\tCurrent Speed: 2000 MHz\n\tStatus: Populated, Enabled\n\tUpgrade: Other\n\tL1 Cache Handle: Not Provided\n\tL2 Cache Handle: Not Provided\n\tL3 Cache Handle: Not Provided\n\nHandle 0x0402, DMI type 4, 32 bytes\nProcessor Information\n\tSocket Designation: CPU 2\n\tType: Central Processor\n\tFamily: Other\n\tManufacturer: Bochs\n\tID: A1 06 02 00 FD FB 8B 17\n\tVersion: Not Specified\n\tVoltage: Unknown\n\tExternal Clock: Unknown\n\tMax Speed: 2000 MHz\n\tCurrent Speed: 2000 MHz\n\tStatus: Populated, Enabled\n\tUpgrade: Other\n\tL1 Cache Handle: Not Provided\n\tL2 Cache Handle: Not Provided\n\tL3 Cache Handle: Not Provided\n\nHandle 0x0037, DMI type 127, 4 bytes.\nEnd Of Table\n'
DMIDECODE_V = '\n# dmidecode 2.12\nSMBIOS 2.4 present.\n364 structures occupying 16870 bytes.\nTable at 0x000E0010.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: Phoenix Technologies LTD\n\tVersion: 6.00\n\tRelease Date: 04/14/2014\n\tAddress: 0xEA050\n\tRuntime Size: 90032 bytes\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tISA is supported\n\t\tPCI is supported\n\t\tPC Card (PCMCIA) is supported\n\t\tPNP is supported\n\t\tAPM is supported\n\t\tBIOS is upgradeable\n\t\tBIOS shadowing is allowed\n\t\tESCD support is available\n\t\tBoot from CD is supported\n\t\tSelectable boot is supported\n\t\tEDD is supported\n\t\tPrint screen service is supported (int 5h)\n\t\t8042 keyboard services are supported (int 9h)\n\t\tSerial services are supported (int 14h)\n\t\tPrinter services are supported (int 17h)\n\t\tCGA/mono video services are supported (int 10h)\n\t\tACPI is supported\n\t\tSmart battery is supported\n\t\tBIOS boot specification is supported\n\t\tFunction key-initiated network boot is supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 4.6\n\tFirmware Revision: 0.0\n\nHandle 0x0001, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: VMware, Inc.\n\tProduct Name: VMware Virtual Platform\n\tVersion: None\n\tSerial Number: VMware-42 10 e9 13 1e 11 e2 21-13 c5 c8 1f 11 42 7c cb\n\tUUID: 4210E913-1E11-E221-13C5-C81F11427CCB\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n'
DMIDECODE_AWS = '\n# dmidecode 2.12-dmifs\nSMBIOS 2.4 present.\n11 structures occupying 310 bytes.\nTable at 0x000EB01F.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: Xen\n\tVersion: 4.2.amazon\n\tRelease Date: 12/09/2016\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tEDD is supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 4.2\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Xen\n\tProduct Name: HVM domU\n\tVersion: 4.2.amazon\n\tSerial Number: ec2f58af-2dad-c57e-88c0-a81cb6084290\n\tUUID: EC2F58AF-2DAD-C57E-88C0-A81CB6084290\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n\nHandle 0x0300, DMI type 3, 13 bytes\nChassis Information\n\tManufacturer: Xen\n\tType: Other\n\tLock: Not Present\n\tVersion: Not Specified\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n'
DMIDECODE_KVM = '\n# dmidecode 3.0\nScanning /dev/mem for entry point.\nSMBIOS 2.8 present.\n13 structures occupying 788 bytes.\nTable at 0xBFFFFCE0.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: SeaBIOS\n\tVersion: 1.9.1-5.el7_3.2\n\tRelease Date: 04/01/2014\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tBIOS characteristics not supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 0.0\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Red Hat\n\tProduct Name: RHEV Hypervisor\n\tVersion: 7.3-7.el7\n\tSerial Number: 34353737-3035-4E43-3734-353130425732\n\tUUID: 10331906-BB22-4716-8876-3DFEF8FA941E\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Red Hat Enterprise Linux\n\nHandle 0x0300, DMI type 3, 21 bytes\nChassis Information\n\tManufacturer: Red Hat\n\tType: Other\n\tLock: Not Present\n\tVersion: RHEL 7.2.0 PC (i440FX + PIIX, 1996)\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n\tOEM Information: 0x00000000\n\tHeight: Unspecified\n\tNumber Of Power Cords: Unspecified\n\tContained Elements: 0\n'
DMIDECODE_FAIL = '# dmidecode 2.11\n# No SMBIOS nor DMI entry point found, sorry.\n'
DMIDECODE_DMI = '\n# dmidecode 2.2\nSMBIOS 2.4 present.\n104 structures occupying 3162 bytes.\nTable at 0x000EE000.\nHandle 0x0000\n\tDMI type 0, 24 bytes.\n\tBIOS Information\n\t\tVendor: HP\n\t\tVersion: A08\n\t\tRelease Date: 09/27/2008\n\t\tAddress: 0xF0000\n\t\tRuntime Size: 64 kB\n\t\tROM Size: 4096 kB\n\t\tCharacteristics:\n\t\t\tPCI is supported\n\t\t\tPNP is supported\n\t\t\tBIOS is upgradeable\n\t\t\tBIOS shadowing is allowed\n\t\t\tESCD support is available\n\t\t\tBoot from CD is supported\n\t\t\tSelectable boot is supported\n\t\t\tEDD is supported\n\t\t\t5.25"/360 KB floppy services are supported (int 13h)\n\t\t\t5.25"/1.2 MB floppy services are supported (int 13h)\n\t\t\t3.5"/720 KB floppy services are supported (int 13h)\n\t\t\tPrint screen service is supported (int 5h)\n\t\t\t8042 keyboard services are supported (int 9h)\n\t\t\tSerial services are supported (int 14h)\n\t\t\tPrinter services are supported (int 17h)\n\t\t\tCGA/mono video services are supported (int 10h)\n\t\t\tACPI is supported\n\t\t\tUSB legacy is supported\n\t\t\tBIOS boot specification is supported\n\t\t\tFunction key-initiated network boot is supported``\nHandle 0x0100\n\tDMI type 1, 27 bytes.\n\tSystem Information\n\t\tManufacturer: HP\n\t\tProduct Name: ProLiant BL685c G1\n\t\tVersion: Not Specified\n\t\tSerial Number: 3H6CMK2537\n\t\tUUID: 58585858-5858-3348-3643-4D4B32353337\n\t\tWake-up Type: Power Switch\n'
DMIDECODE_ODDITIES = '\nHandle 0x0009, DMI type 129, 8 bytes\nOEM-specific Type\n\tHeader and Data:\n\t\t81 08 09 00 01 01 02 01\n\tStrings:\n\t\tIntel_ASF\n\t\tIntel_ASF_001\n\nHandle 0x000A, DMI type 134, 13 bytes\nOEM-specific Type\n\tHeader and Data:\n\t\t86 0D 0A 00 28 06 14 20 00 00 00 00 00\n\nHandle 0x000F, DMI type 8, 9 bytes\nPort Connector Information\n\tInternal Reference Designator: Not Available\n\tInternal Connector Type: None\n\tExternal Reference Designator: USB 1\n\tExternal Connector Type: Access Bus (USB)\n\tPort Type: USB\n\nHandle 0x0010, DMI type 8, 9 bytes\nPort Connector Information\n\tInternal Reference Designator: Not Available\n\tInternal Connector Type: None\n\tExternal Reference Designator: USB 2\n\tExternal Connector Type: Access Bus (USB)\n\tPort Type: USB\n\nHandle 0x0029, DMI type 13, 22 bytes\nBIOS Language Information\n\tLanguage Description Format: Abbreviated\n\tInstallable Languages: 1\n\t\ten-US\n\tCurrently Installed Language: en-US\n\nHandle 0x000A, DMI type 134, 13 bytes\nOEM-specific Type\n\tHeader and Data:\n\t\t01 02 03 04 05 06 07 08\n\n'

def test_get_dmidecode():
    """
    Test for three kinds of output format of dmidecode parser
    """
    context = context_wrap(DMIDECODE)
    ret = DMIDecode(context)
    assert len(ret.get('bios_information')) == 1
    assert ret.get('bios_information')[0].get('vendor') == 'HP'
    assert ret.get('bios_information')[0].get('version') == 'P70'
    assert ret.get('bios_information')[0].get('release_date') == '03/01/2013'
    assert ret.get('bios_information')[0].get('address') == '0xF0000'
    assert ret.get('bios_information')[0].get('runtime_size') == '64 kB'
    assert ret.get('bios_information')[0].get('rom_size') == '8192 kB'
    tmp = [
     'PCI is supported', 'PNP is supported', 'BIOS is upgradeable',
     'BIOS shadowing is allowed', 'ESCD support is available',
     'Boot from CD is supported', 'Selectable boot is supported',
     'EDD is supported',
     '5.25"/360 kB floppy services are supported (int 13h)',
     '5.25"/1.2 MB floppy services are supported (int 13h)',
     '3.5"/720 kB floppy services are supported (int 13h)',
     'Print screen service is supported (int 5h)',
     'j042 keyboard services are supported (int 9h)',
     'Serial services are supported (int 14h)',
     'Printer services are supported (int 17h)',
     'CGA/mono video services are supported (int 10h)',
     'ACPI is supported', 'USB legacy is supported',
     'BIOS boot specification is supported',
     'Function key-initiated network boot is supported',
     'Targeted content distribution is supported']
    assert ret.get('bios_information')[0].get('characteristics') == tmp
    assert ret.get('bios_information')[0].get('firmware_revision') == '1.22'
    assert len(ret.get('system_information')) == 1
    assert ret.get('system_information')[0].get('manufacturer') == 'HP'
    assert ret.get('system_information')[0].get('product_name') == 'ProLiant DL380p Gen8'
    assert ret.get('system_information')[0].get('version') == 'Not Specified'
    assert ret.get('system_information')[0].get('serial_number') == '2M23360006'
    assert ret.get('system_information')[0].get('uuid') == '34373936-3439-4D32-3233-333630303036'
    assert ret.get('system_information')[0].get('wake-up_type') == 'Power Switch'
    assert ret.get('system_information')[0].get('sku_number') == '697494-S01'
    assert ret.get('system_information')[0].get('family') == 'ProLiant'
    assert len(ret.get('chassis_information')) == 1
    assert ret.get('chassis_information')[0].get('manufacturer') == 'hp'
    assert ret.get('chassis_information')[0].get('type') == 'rack mount chassis'
    assert ret.get('chassis_information')[0].get('lock') == 'not present'
    assert ret.get('chassis_information')[0].get('version') == 'not specified'
    assert ret.get('chassis_information')[0].get('serial_number') == '2m23360006'
    assert ret.get('chassis_information')[0].get('asset_tag') == ''
    assert ret.get('chassis_information')[0].get('boot-up_state') == 'Safe'
    assert ret.get('chassis_information')[0].get('power_supply_state') == 'Safe'
    assert ret.get('chassis_information')[0].get('thermal_state') == 'Safe'
    assert ret.get('chassis_information')[0].get('security_status') == 'Unknown'
    assert ret.get('chassis_information')[0].get('oem_information') == '0x00000000'
    assert ret.get('chassis_information')[0].get('height') == '2 U'
    assert ret.get('chassis_information')[0].get('number_of_power_cords') == '2'
    assert ret.get('chassis_information')[0].get('manufacturer') == 'hp'
    assert ret.get('chassis_information')[0].get('contained_elements') == '0'
    assert len(ret.get('processor_information')) == 2
    assert ret.get('processor_information')[0].get('socket_designation') == 'CPU 1'
    assert ret.get('processor_information')[0].get('type') == 'Central Processor'
    assert ret.get('processor_information')[1].get('socket_designation') == 'CPU 2'
    assert ret.get('processor_information')[1].get('type') == 'Central Processor'
    assert 'table_at_0xbffcb000.' not in ret
    assert ret.system_info == ret['system_information'][0]
    assert ret.bios == ret['bios_information'][0]
    assert ret.bios_vendor == 'HP'
    assert ret.bios_date == date(2013, 3, 1)
    assert ret.processor_manufacturer == 'Bochs'


def test_get_dmidecode_fail():
    """
    Test for faied raw data
    """
    context = context_wrap(DMIDECODE_FAIL)
    ret = DMIDecode(context)
    assert ret.is_present is False


def test_get_dmidecode_dmi():
    """
    Test for three kinds of output format of dmidecode parser
    with special input format:
    "
        DMI" in the input
    """
    context = context_wrap(DMIDECODE_DMI)
    ret = DMIDecode(context)
    assert ret.get('bios_information')[0].get('vendor') == 'HP'
    assert ret.get('bios_information')[0].get('version') == 'A08'
    assert ret.get('bios_information')[0].get('release_date') == '09/27/2008'
    assert ret.get('bios_information')[0].get('address') == '0xF0000'
    assert ret.get('bios_information')[0].get('runtime_size') == '64 kB'
    assert ret.get('bios_information')[0].get('rom_size') == '4096 kB'
    tmp = [
     'PCI is supported', 'PNP is supported', 'BIOS is upgradeable',
     'BIOS shadowing is allowed', 'ESCD support is available',
     'Boot from CD is supported', 'Selectable boot is supported',
     'EDD is supported',
     '5.25"/360 KB floppy services are supported (int 13h)',
     '5.25"/1.2 MB floppy services are supported (int 13h)',
     '3.5"/720 KB floppy services are supported (int 13h)',
     'Print screen service is supported (int 5h)',
     '8042 keyboard services are supported (int 9h)',
     'Serial services are supported (int 14h)',
     'Printer services are supported (int 17h)',
     'CGA/mono video services are supported (int 10h)',
     'ACPI is supported', 'USB legacy is supported',
     'BIOS boot specification is supported',
     'Function key-initiated network boot is supported``']
    assert ret.get('bios_information')[0].get('characteristics') == tmp
    assert ret.get('system_information')[0].get('manufacturer') == 'HP'
    assert ret.get('system_information')[0].get('product_name') == 'ProLiant BL685c G1'
    assert ret.get('system_information')[0].get('version') == 'Not Specified'
    assert ret.get('system_information')[0].get('serial_number') == '3H6CMK2537'
    assert ret.get('system_information')[0].get('uuid') == '58585858-5858-3348-3643-4D4B32353337'
    assert ret.get('system_information')[0].get('wake-up_type') == 'Power Switch'


def test_dmidecode_oddities():
    dmi = DMIDecode(context_wrap(DMIDECODE_ODDITIES))
    assert len(dmi['oem-specific_type']) == 3
    assert dmi['oem-specific_type'][0] == {'header_and_data': '81 08 09 00 01 01 02 01', 
       'strings': [
                 'Intel_ASF', 'Intel_ASF_001']}
    assert dmi['oem-specific_type'][1] == {'header_and_data': '86 0D 0A 00 28 06 14 20 00 00 00 00 00'}
    assert dmi['oem-specific_type'][2] == {'header_and_data': '01 02 03 04 05 06 07 08'}
    assert len(dmi['port_connector_information']) == 2
    assert dmi['port_connector_information'][0] == {'internal_reference_designator': 'Not Available', 
       'internal_connector_type': 'None', 
       'external_reference_designator': 'USB 1', 
       'external_connector_type': 'Access Bus (USB)', 
       'port_type': 'USB'}
    assert dmi['port_connector_information'][0] == {'internal_reference_designator': 'Not Available', 
       'internal_connector_type': 'None', 
       'external_reference_designator': 'USB 1', 
       'external_connector_type': 'Access Bus (USB)', 
       'port_type': 'USB'}
    assert len(dmi['bios_language_information']) == 1
    assert dmi['bios_language_information'][0] == {'language_description_format': 'Abbreviated', 
       'installable_languages': [
                               '1', 'en-US'], 
       'currently_installed_language': 'en-US'}
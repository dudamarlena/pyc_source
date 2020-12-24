# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_cloud_provider.py
# Compiled at: 2020-03-25 13:10:41
import doctest
from insights.combiners import cloud_provider
from insights.combiners.cloud_provider import CloudProvider
from insights.parsers.installed_rpms import InstalledRpms as IRPMS
from insights.parsers.dmidecode import DMIDecode
from insights.parsers.yum import YumRepoList
from insights.tests import context_wrap
RPMS = ('\ngnome-terminal-3.28.2-2.fc28.x86_64\npython3-IPy-0.81-21.fc28.noarch\ngnu-free-serif-fonts-20120503-17.fc28.noarch\n').strip()
RPMS_AWS = ('\ngnome-terminal-3.28.2-2.fc28.x86_64\npython3-IPy-0.81-21.fc28.noarch\ngnu-free-serif-fonts-20120503-17.fc28.noarch\nrh-amazon-rhui-client-2.2.124-1.el7\n').strip()
RPMS_GOOGLE = ('\ngnome-terminal-3.28.2-2.fc28.x86_64\npython3-IPy-0.81-21.fc28.noarch\ngnu-free-serif-fonts-20120503-17.fc28.noarch\ngoogle-rhui-client-5.1.100-1.el7\ngoogle-rhui-client-5.1.100-1.el6\n').strip()
RPMS_AZURE = ('\ngnome-terminal-3.28.2-2.fc28.x86_64\npython3-IPy-0.81-21.fc28.noarch\ngnu-free-serif-fonts-20120503-17.fc28.noarch\nWALinuxAgent-2.2.18-1.el7\n').strip()
YUM_REPOLIST_AZURE = ('\nLoaded plugins: enabled_repos_upload, package_upload, product-id, search-\n              : disabled-repos, security, subscription-manager\nrepo id                                repo name                          status\nrhel-6-server-rpms                     Red Hat Enterprise Linux 6 Server  20584\nrhel-6-server-satellite-tools-6.3-rpms Red Hat Satellite Tools 6.3 (for R    40\nrhui-microsoft-azure-rhel7-2.2-74      Red Hat Software Collect             600\nrepolist: 21224\nUploading Enabled Repositories Report\nLoaded plugins: product-id, subscription-manager\n').strip()
YUM_REPOLIST_NOT_AZURE = ('\nLoaded plugins: enabled_repos_upload, package_upload, product-id, search-\n              : disabled-repos, security, subscription-manager\nrepo id                                repo name                          status\nrhel-6-server-rpms                     Red Hat Enterprise Linux 6 Server  20584\nrhel-6-server-satellite-tools-6.3-rpms Red Hat Satellite Tools 6.3 (for R    40\nrepolist: 21224\nUploading Enabled Repositories Report\nLoaded plugins: product-id, subscription-manager\n').strip()
DMIDECODE = '\n# dmidecode 2.11\nSMBIOS 2.7 present.\n188 structures occupying 5463 bytes.\nTable at 0xBFFCB000.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: HP\n\tVersion: P70\n\tRelease Date: 03/01/2013\n\tAddress: 0xF0000\n\tRuntime Size: 64 kB\n\tROM Size: 8192 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tPNP is supported\n\t\tBIOS is upgradeable\n\t\tBIOS shadowing is allowed\n\t\tESCD support is available\n\t\tBoot from CD is supported\n\t\tSelectable boot is supported\n\t\tEDD is supported\n\t\t5.25"/360 kB floppy services are supported (int 13h)\n\t\t5.25"/1.2 MB floppy services are supported (int 13h)\n\t\t3.5"/720 kB floppy services are supported (int 13h)\n\t\tPrint screen service is supported (int 5h)\n\t\tj042 keyboard services are supported (int 9h)\n\t\tSerial services are supported (int 14h)\n\t\tPrinter services are supported (int 17h)\n\t\tCGA/mono video services are supported (int 10h)\n\t\tACPI is supported\n\t\tUSB legacy is supported\n\t\tBIOS boot specification is supported\n\t\tFunction key-initiated network boot is supported\n\t\tTargeted content distribution is supported\n\tFirmware Revision: 1.22\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: HP\n\tProduct Name: ProLiant DL380p Gen8\n\tVersion: Not Specified\n\tSerial Number: 2M23360006\n\tUUID: 34373936-3439-4D32-3233-333630303036\n\tWake-up Type: Power Switch\n\tSKU Number: 697494-S01\n\tFamily: ProLiant\n\nHandle 0x0300, DMI type 3, 21 bytes\nchassis information\n\tmanufacturer: hp\n\ttype: rack mount chassis\n\tlock: not present\n\tversion: not specified\n\tserial number: 2m23360006\n\tasset Tag:\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n\tOEM Information: 0x00000000\n\tHeight: 2 U\n\tNumber Of Power Cords: 2\n\tContained Elements: 0\n\nHandle 0x0401, DMI type 4, 32 bytes\nProcessor Information\n\tSocket Designation: CPU 1\n\tType: Central Processor\n\tFamily: Other\n\tManufacturer: Bochs\n\tID: A1 06 02 00 FD FB 8B 17\n\tVersion: Not Specified\n\tVoltage: Unknown\n\tExternal Clock: Unknown\n\tMax Speed: 2000 MHz\n\tCurrent Speed: 2000 MHz\n\tStatus: Populated, Enabled\n\tUpgrade: Other\n\tL1 Cache Handle: Not Provided\n\tL2 Cache Handle: Not Provided\n\tL3 Cache Handle: Not Provided\n\nHandle 0x0402, DMI type 4, 32 bytes\nProcessor Information\n\tSocket Designation: CPU 2\n\tType: Central Processor\n\tFamily: Other\n\tManufacturer: Bochs\n\tID: A1 06 02 00 FD FB 8B 17\n\tVersion: Not Specified\n\tVoltage: Unknown\n\tExternal Clock: Unknown\n\tMax Speed: 2000 MHz\n\tCurrent Speed: 2000 MHz\n\tStatus: Populated, Enabled\n\tUpgrade: Other\n\tL1 Cache Handle: Not Provided\n\tL2 Cache Handle: Not Provided\n\tL3 Cache Handle: Not Provided\n\nHandle 0x0037, DMI type 127, 4 bytes.\nEnd Of Table\n'
DMIDECODE_BARE_METAL = ('\n# dmidecode 3.0\nGetting SMBIOS data from sysfs.\nSMBIOS 2.7 present.\n56 structures occupying 2407 bytes.\nTable at 0x000EB4C0.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: American Megatrends Inc.\n\tVersion: 2.0a\n\tRelease Date: 06/08/2012\n\tAddress: 0xF0000\n\tRuntime Size: 64 kB\n\tROM Size: 8192 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tBIOS is upgradeable\n\t\tBIOS shadowing is allowed\n\t\tBoot from CD is supported\n\t\tSelectable boot is supported\n\t\tBIOS ROM is socketed\n\t\tEDD is supported\n\t\t5.25"/1.2 MB floppy services are supported (int 13h)\n\t\t3.5"/720 kB floppy services are supported (int 13h)\n\t\t3.5"/2.88 MB floppy services are supported (int 13h)\n\t\tPrint screen service is supported (int 5h)\n\t\t8042 keyboard services are supported (int 9h)\n\t\tSerial services are supported (int 14h)\n\t\tPrinter services are supported (int 17h)\n\t\tACPI is supported\n\t\tUSB legacy is supported\n\t\tBIOS boot specification is supported\n\t\tFunction key-initiated network boot is supported\n\t\tTargeted content distribution is supported\n\t\tUEFI is supported\n\tBIOS Revision: 2.10\n\nHandle 0x0001, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Supermicro\n\tProduct Name: X9SCL/X9SCM\n\tVersion: 0123456789\n\tSerial Number: 0123456789\n\tUUID: 12345678-1234-1234-1234-123456681234\n\tWake-up Type: Power Switch\n\tSKU Number: To be filled by O.E.M.\n\tFamily: To be filled by O.E.M.\n\nHandle 0x0002, DMI type 2, 15 bytes\nBase Board Information\n\tManufacturer: Supermicro\n\tProduct Name: X9SCL/X9SCM\n\tVersion: 0123456789\n\tSerial Number: 1234567812\n\tAsset Tag: To be filled by O.E.M.\n\tFeatures:\n\t\tBoard is a hosting board\n\t\tBoard is replaceable\n\tLocation In Chassis: To be filled by O.E.M.\n\tChassis Handle: 0x0003\n\tType: Motherboard\n\tContained Object Handles: 0\n').strip()
DMIDECODE_AWS = '\n# dmidecode 2.12-dmifs\nSMBIOS 2.4 present.\n11 structures occupying 310 bytes.\nTable at 0x000EB01F.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: Xen\n\tVersion: 4.2.amazon\n\tRelease Date: 12/09/2016\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tEDD is supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 4.2\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Xen\n\tProduct Name: HVM domU\n\tVersion: 4.2.amazon\n\tSerial Number: ec2f58af-2dad-c57e-88c0-a81cb6084290\n\tUUID: EC2F58AF-2DAD-C57E-88C0-A81CB6084290\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n\nHandle 0x0300, DMI type 3, 13 bytes\nChassis Information\n\tManufacturer: Xen\n\tType: Other\n\tLock: Not Present\n\tVersion: Not Specified\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n'
DMIDECODE_AWS_UUID = '\n# dmidecode 2.12-dmifs\nSMBIOS 2.4 present.\n11 structures occupying 310 bytes.\nTable at 0x000EB01F.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: Xen\n\tVersion: 4.2\n\tRelease Date: 12/09/2016\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tEDD is supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 4.2\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Xen\n\tProduct Name: HVM domU\n\tVersion: 4.2.amazon\n\tSerial Number: ec2f58af-2dad-c57e-88c0-a81cb6084290\n\tUUID: EC2F58AF-2DAD-C57E-88C0-A81CB6084290\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n\nHandle 0x0300, DMI type 3, 13 bytes\nChassis Information\n\tManufacturer: Xen\n\tType: Other\n\tLock: Not Present\n\tVersion: Not Specified\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n'
DMIDECODE_GOOGLE = '\n# dmidecode 2.12-dmifs\nSMBIOS 2.4 present.\n11 structures occupying 310 bytes.\nTable at 0x000EB01F.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: Google\n\tVersion: Google\n\tRelease Date: 12/09/2016\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tPCI is supported\n\t\tEDD is supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 4.2\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Xen\n\tProduct Name: HVM domU\n\tVersion: 4.2.amazon\n\tSerial Number: ec2f58af-2dad-c57e-88c0-a81cb6084290\n\tUUID: EC2F58AF-2DAD-C57E-88C0-A81CB6084290\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n\nHandle 0x0300, DMI type 3, 13 bytes\nChassis Information\n\tManufacturer: Xen\n\tType: Other\n\tLock: Not Present\n\tVersion: Not Specified\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n'
DMIDECODE_AZURE_ASSET_TAG = '\n# dmidecode 3.1\nGetting SMBIOS data from sysfs.\nSMBIOS 2.8 present.\n10 structures occupying 511 bytes.\nTable at 0x000F6050.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: SeaBIOS\n\tVersion: 1.11.0-2.el7\n\tRelease Date: 04/01/2014\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tBIOS characteristics not supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 0.0\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: oVirt\n\tProduct Name: oVirt Node\n\tVersion: 7-5.1804.4.el7.centos\n\tSerial Number: 30393137-3436-584D-5136-323830304E46\n\tUUID: a35ae32b-ed0a-49a4-9dbb-eecf21f88aab\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Red Hat Enterprise Linux\n\nHandle 0x0300, DMI type 3, 21 bytes\nChassis Information\n\tManufacturer: Red Hat\n\tType: Other\n\tLock: Not Present\n\tVersion: RHEL 7.2.0 PC (i440FX + PIIX, 1996)\n\tSerial Number: Not Specified\n\tAsset Tag: 7783-7084-3265-9085-8269-3286-77\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n\tOEM Information: 0x00000000\n\tHeight: Unspecified\n\tNumber Of Power Cords: Unspecified\n\tContained Elements: 0\n'
DMIDECODE_FAIL = '# dmidecode 2.11\n# No SMBIOS nor DMI entry point found, sorry.\n'
DMIDECODE_ALIBABA = '\n# dmidecode 3.2\nGetting SMBIOS data from sysfs.\nSMBIOS 2.8 present.\n11 structures occupying 524 bytes.\nTable at 0x000F4AC0.\n\nHandle 0x0000, DMI type 0, 24 bytes\nBIOS Information\n\tVendor: SeaBIOS\n\tVersion: ab23bb1\n\tRelease Date: 04/01/2014\n\tAddress: 0xE8000\n\tRuntime Size: 96 kB\n\tROM Size: 64 kB\n\tCharacteristics:\n\t\tBIOS characteristics not supported\n\t\tTargeted content distribution is supported\n\tBIOS Revision: 0.0\n\nHandle 0x0100, DMI type 1, 27 bytes\nSystem Information\n\tManufacturer: Alibaba Cloud\n\tProduct Name: Alibaba Cloud ECS\n\tVersion: pc-i440fx-2.1\n\tSerial Number: 1111111a-2220-333c-4449-555555555552\n\tUUID: 1111111a-2220-333c-4449-555555555552\n\tWake-up Type: Power Switch\n\tSKU Number: Not Specified\n\tFamily: Not Specified\n\nHandle 0x0300, DMI type 3, 21 bytes\nChassis Information\n\tManufacturer: Alibaba Cloud\n\tType: Other\n\tLock: Not Present\n\tVersion: pc-i440fx-2.1\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tBoot-up State: Safe\n\tPower Supply State: Safe\n\tThermal State: Safe\n\tSecurity Status: Unknown\n\tOEM Information: 0x00000000\n\tHeight: Unspecified\n\tNumber Of Power Cords: Unspecified\n\tContained Elements: 0\n\nHandle 0x0400, DMI type 4, 42 bytes\nProcessor Information\n\tSocket Designation: CPU 0\n\tType: Central Processor\n\tFamily: Other\n\tManufacturer: Alibaba Cloud\n\tID: 11 22 33 44 55 66 77 FF\n\tVersion: pc-i440fx-2.1\n\tVoltage: Unknown\n\tExternal Clock: Unknown\n\tMax Speed: Unknown\n\tCurrent Speed: Unknown\n\tStatus: Populated, Enabled\n\tUpgrade: Other\n\tL1 Cache Handle: Not Provided\n\tL2 Cache Handle: Not Provided\n\tL3 Cache Handle: Not Provided\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tPart Number: Not Specified\n\tCore Count: 2\n\tCore Enabled: 2\n\tThread Count: 2\n\tCharacteristics: None\n\nHandle 0x1000, DMI type 16, 23 bytes\nPhysical Memory Array\n\tLocation: Other\n\tUse: System Memory\n\tError Correction Type: Multi-bit ECC\n\tMaximum Capacity: 32 GB\n\tError Information Handle: Not Provided\n\tNumber Of Devices: 2\n\nHandle 0x1100, DMI type 17, 40 bytes\nMemory Device\n\tArray Handle: 0x1000\n\tError Information Handle: Not Provided\n\tTotal Width: Unknown\n\tData Width: Unknown\n\tSize: 16384 MB\n\tForm Factor: DIMM\n\tSet: None\n\tLocator: DIMM 0\n\tBank Locator: Not Specified\n\tType: RAM\n\tType Detail: Other\n\tSpeed: Unknown\n\tManufacturer: Alibaba Cloud\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tPart Number: Not Specified\n\tRank: Unknown\n\tConfigured Memory Speed: Unknown\n\tMinimum Voltage: Unknown\n\tMaximum Voltage: Unknown\n\tConfigured Voltage: Unknown\n\nHandle 0x1101, DMI type 17, 40 bytes\nMemory Device\n\tArray Handle: 0x1000\n\tError Information Handle: Not Provided\n\tTotal Width: Unknown\n\tData Width: Unknown\n\tSize: 16384 MB\n\tForm Factor: DIMM\n\tSet: None\n\tLocator: DIMM 1\n\tBank Locator: Not Specified\n\tType: RAM\n\tType Detail: Other\n\tSpeed: Unknown\n\tManufacturer: Alibaba Cloud\n\tSerial Number: Not Specified\n\tAsset Tag: Not Specified\n\tPart Number: Not Specified\n\tRank: Unknown\n\tConfigured Memory Speed: Unknown\n\tMinimum Voltage: Unknown\n\tMaximum Voltage: Unknown\n\tConfigured Voltage: Unknown\n\nHandle 0x1300, DMI type 19, 31 bytes\nMemory Array Mapped Address\n\tStarting Address: 0x00000000000\n\tEnding Address: 0x000BFFFFFFF\n\tRange Size: 3 GB\n\tPhysical Array Handle: 0x1000\n\tPartition Width: 1\n\nHandle 0x1301, DMI type 19, 31 bytes\nMemory Array Mapped Address\n\tStarting Address: 0x00100000000\n\tEnding Address: 0x0083FFFFFFF\n\tRange Size: 29 GB\n\tPhysical Array Handle: 0x1000\n\tPartition Width: 1\n\nHandle 0x2000, DMI type 32, 11 bytes\nSystem Boot Information\n\tStatus: No errors detected\n\nHandle 0x7F00, DMI type 127, 4 bytes\nEnd Of Table\n'

def test_rpm_google():
    irpms = IRPMS(context_wrap(RPMS_GOOGLE))
    dmi = DMIDecode(context_wrap(DMIDECODE))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.GOOGLE
    assert 'google-rhui-client-5.1.100-1.el7' in ret.cp_rpms.get(CloudProvider.GOOGLE)
    assert 'google-rhui-client-5.1.100-1.el6' in ret.cp_rpms.get(CloudProvider.GOOGLE)


def test_rpm_aws():
    irpms = IRPMS(context_wrap(RPMS_AWS))
    dmi = DMIDecode(context_wrap(DMIDECODE))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AWS
    assert ret.cp_rpms.get(CloudProvider.AWS)[0] == 'rh-amazon-rhui-client-2.2.124-1.el7'


def test_rpm_azure():
    irpms = IRPMS(context_wrap(RPMS_AZURE))
    dmi = DMIDecode(context_wrap(DMIDECODE_BARE_METAL))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AZURE
    assert ret.cp_rpms.get(CloudProvider.AZURE)[0] == 'WALinuxAgent-2.2.18-1.el7'


def test__yum_azure():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AZURE
    assert 'rhui-microsoft-azure-rhel7-2.2-74' in ret.cp_yum.get(CloudProvider.AZURE)


def test__bios_version_aws():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE_AWS))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AWS
    assert ret.cp_bios_version[CloudProvider.AWS] == '4.2.amazon'


def test__bios_vendor_google():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE_GOOGLE))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.GOOGLE
    assert ret.cp_bios_vendor[CloudProvider.GOOGLE] == 'Google'


def test__asset_tag_azure():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE_AZURE_ASSET_TAG))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AZURE
    assert ret.cp_asset_tag[CloudProvider.AZURE] == '7783-7084-3265-9085-8269-3286-77'


def test__uuid():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE_AWS_UUID))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.AWS
    assert ret.cp_uuid[CloudProvider.AWS] == 'EC2F58AF-2DAD-C57E-88C0-A81CB6084290'


def test_dmidecode_alibaba():
    irpms = IRPMS(context_wrap(RPMS))
    dmi = DMIDecode(context_wrap(DMIDECODE_ALIBABA))
    yrl = YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE))
    ret = CloudProvider(irpms, dmi, yrl)
    assert ret.cloud_provider == CloudProvider.ALIBABA
    assert ret.cp_manufacturer[CloudProvider.ALIBABA] == 'Alibaba Cloud'


def test_docs():
    cp_aws = CloudProvider(IRPMS(context_wrap(RPMS_AWS)), DMIDecode(context_wrap(DMIDECODE_AWS)), YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE)))
    cp_azure = CloudProvider(IRPMS(context_wrap(RPMS_AZURE)), DMIDecode(context_wrap(DMIDECODE_AZURE_ASSET_TAG)), YumRepoList(context_wrap(YUM_REPOLIST_AZURE)))
    cp_alibaba = CloudProvider(IRPMS(context_wrap(RPMS)), DMIDecode(context_wrap(DMIDECODE_ALIBABA)), YumRepoList(context_wrap(YUM_REPOLIST_NOT_AZURE)))
    env = {'cp_aws': cp_aws, 
       'cp_azure': cp_azure, 
       'cp_alibaba': cp_alibaba}
    failed, total = doctest.testmod(cloud_provider, globs=env)
    assert failed == 0
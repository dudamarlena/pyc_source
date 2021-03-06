# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp_mibs/HOST-RESOURCES-TYPES.py
# Compiled at: 2016-02-13 18:15:18
(OctetString, ObjectIdentifier, Integer) = mibBuilder.importSymbols('ASN1', 'OctetString', 'ObjectIdentifier', 'Integer')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(SingleValueConstraint, ValueSizeConstraint, ConstraintsIntersection, ValueRangeConstraint, ConstraintsUnion) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'SingleValueConstraint', 'ValueSizeConstraint', 'ConstraintsIntersection', 'ValueRangeConstraint', 'ConstraintsUnion')
(hrStorage, hrMIBAdminInfo, hrDevice) = mibBuilder.importSymbols('HOST-RESOURCES-MIB', 'hrStorage', 'hrMIBAdminInfo', 'hrDevice')
(ModuleCompliance, NotificationGroup) = mibBuilder.importSymbols('SNMPv2-CONF', 'ModuleCompliance', 'NotificationGroup')
(Gauge32, Bits, Integer32, TimeTicks, MibScalar, MibTable, MibTableRow, MibTableColumn, MibIdentifier, Counter32, Counter64, iso, ObjectIdentity, NotificationType, IpAddress, Unsigned32, ModuleIdentity) = mibBuilder.importSymbols('SNMPv2-SMI', 'Gauge32', 'Bits', 'Integer32', 'TimeTicks', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'MibIdentifier', 'Counter32', 'Counter64', 'iso', 'ObjectIdentity', 'NotificationType', 'IpAddress', 'Unsigned32', 'ModuleIdentity')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
hostResourcesTypesModule = ModuleIdentity((1, 3, 6, 1, 2, 1, 25, 7, 4)).setRevisions(('2000-03-06 00:00', ))
if mibBuilder.loadTexts:
    hostResourcesTypesModule.setLastUpdated('200003060000Z')
if mibBuilder.loadTexts:
    hostResourcesTypesModule.setOrganization('IETF Host Resources MIB Working Group')
if mibBuilder.loadTexts:
    hostResourcesTypesModule.setContactInfo('Steve Waldbusser\n         Postal: Lucent Technologies, Inc.\n                 1213 Innsbruck Dr.\n                 Sunnyvale, CA 94089\n                 USA\n         Phone: 650-318-1251\n         Fax:   650-318-1633\n         Email: waldbusser@ins.com\n\n         In addition, the Host Resources MIB mailing list is dedicated\n         to discussion of this MIB. To join the mailing list, send a\n         request message to hostmib-request@andrew.cmu.edu. The mailing\n         list address is hostmib@andrew.cmu.edu.')
if mibBuilder.loadTexts:
    hostResourcesTypesModule.setDescription('This MIB module registers type definitions for\n         storage types, device types, and file system types.\n         After the initial revision, this module will be\n         maintained by IANA.')
hrStorageTypes = MibIdentifier((1, 3, 6, 1, 2, 1, 25, 2, 1))
hrStorageOther = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 1))
if mibBuilder.loadTexts:
    hrStorageOther.setDescription('The storage type identifier used when no other defined\n           type is appropriate.')
hrStorageRam = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 2))
if mibBuilder.loadTexts:
    hrStorageRam.setDescription('The storage type identifier used for RAM.')
hrStorageVirtualMemory = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 3))
if mibBuilder.loadTexts:
    hrStorageVirtualMemory.setDescription('The storage type identifier used for virtual memory,\n           temporary storage of swapped or paged memory.')
hrStorageFixedDisk = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 4))
if mibBuilder.loadTexts:
    hrStorageFixedDisk.setDescription('The storage type identifier used for non-removable\n           rigid rotating magnetic storage devices.')
hrStorageRemovableDisk = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 5))
if mibBuilder.loadTexts:
    hrStorageRemovableDisk.setDescription('The storage type identifier used for removable rigid\n           rotating magnetic storage devices.')
hrStorageFloppyDisk = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 6))
if mibBuilder.loadTexts:
    hrStorageFloppyDisk.setDescription('The storage type identifier used for non-rigid rotating\n           magnetic storage devices.')
hrStorageCompactDisc = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 7))
if mibBuilder.loadTexts:
    hrStorageCompactDisc.setDescription('The storage type identifier used for read-only rotating\n           optical storage devices.')
hrStorageRamDisk = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 8))
if mibBuilder.loadTexts:
    hrStorageRamDisk.setDescription('The storage type identifier used for a file system that\n           is stored in RAM.')
hrStorageFlashMemory = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 9))
if mibBuilder.loadTexts:
    hrStorageFlashMemory.setDescription('The storage type identifier used for flash memory.')
hrStorageNetworkDisk = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 2, 1, 10))
if mibBuilder.loadTexts:
    hrStorageNetworkDisk.setDescription('The storage type identifier used for a\n           networked file system.')
hrDeviceTypes = MibIdentifier((1, 3, 6, 1, 2, 1, 25, 3, 1))
hrDeviceOther = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 1))
if mibBuilder.loadTexts:
    hrDeviceOther.setDescription('The device type identifier used when no other defined\n           type is appropriate.')
hrDeviceUnknown = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 2))
if mibBuilder.loadTexts:
    hrDeviceUnknown.setDescription('The device type identifier used when the device type is\n           unknown.')
hrDeviceProcessor = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 3))
if mibBuilder.loadTexts:
    hrDeviceProcessor.setDescription('The device type identifier used for a CPU.')
hrDeviceNetwork = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 4))
if mibBuilder.loadTexts:
    hrDeviceNetwork.setDescription('The device type identifier used for a network interface.')
hrDevicePrinter = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 5))
if mibBuilder.loadTexts:
    hrDevicePrinter.setDescription('The device type identifier used for a printer.')
hrDeviceDiskStorage = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 6))
if mibBuilder.loadTexts:
    hrDeviceDiskStorage.setDescription('The device type identifier used for a disk drive.')
hrDeviceVideo = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 10))
if mibBuilder.loadTexts:
    hrDeviceVideo.setDescription('The device type identifier used for a video device.')
hrDeviceAudio = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 11))
if mibBuilder.loadTexts:
    hrDeviceAudio.setDescription('The device type identifier used for an audio device.')
hrDeviceCoprocessor = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 12))
if mibBuilder.loadTexts:
    hrDeviceCoprocessor.setDescription('The device type identifier used for a co-processor.')
hrDeviceKeyboard = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 13))
if mibBuilder.loadTexts:
    hrDeviceKeyboard.setDescription('The device type identifier used for a keyboard device.')
hrDeviceModem = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 14))
if mibBuilder.loadTexts:
    hrDeviceModem.setDescription('The device type identifier used for a modem.')
hrDeviceParallelPort = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 15))
if mibBuilder.loadTexts:
    hrDeviceParallelPort.setDescription('The device type identifier used for a parallel port.')
hrDevicePointing = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 16))
if mibBuilder.loadTexts:
    hrDevicePointing.setDescription('The device type identifier used for a pointing device\n           (e.g., a mouse).')
hrDeviceSerialPort = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 17))
if mibBuilder.loadTexts:
    hrDeviceSerialPort.setDescription('The device type identifier used for a serial port.')
hrDeviceTape = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 18))
if mibBuilder.loadTexts:
    hrDeviceTape.setDescription('The device type identifier used for a tape storage device.')
hrDeviceClock = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 19))
if mibBuilder.loadTexts:
    hrDeviceClock.setDescription('The device type identifier used for a clock device.')
hrDeviceVolatileMemory = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 20))
if mibBuilder.loadTexts:
    hrDeviceVolatileMemory.setDescription('The device type identifier used for a volatile memory\n           storage device.')
hrDeviceNonVolatileMemory = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 1, 21))
if mibBuilder.loadTexts:
    hrDeviceNonVolatileMemory.setDescription('The device type identifier used for a non-volatile memory\n           storage device.')
hrFSTypes = MibIdentifier((1, 3, 6, 1, 2, 1, 25, 3, 9))
hrFSOther = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 1))
if mibBuilder.loadTexts:
    hrFSOther.setDescription('The file system type identifier used when no other\n           defined type is appropriate.')
hrFSUnknown = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 2))
if mibBuilder.loadTexts:
    hrFSUnknown.setDescription('The file system type identifier used when the type of\n           file system is unknown.')
hrFSBerkeleyFFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 3))
if mibBuilder.loadTexts:
    hrFSBerkeleyFFS.setDescription('The file system type identifier used for the\n           Berkeley Fast File System.')
hrFSSys5FS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 4))
if mibBuilder.loadTexts:
    hrFSSys5FS.setDescription('The file system type identifier used for the\n           System V File System.')
hrFSFat = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 5))
if mibBuilder.loadTexts:
    hrFSFat.setDescription("The file system type identifier used for\n           DOS's FAT file system.")
hrFSHPFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 6))
if mibBuilder.loadTexts:
    hrFSHPFS.setDescription("The file system type identifier used for OS/2's\n           High Performance File System.")
hrFSHFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 7))
if mibBuilder.loadTexts:
    hrFSHFS.setDescription('The file system type identifier used for the\n           Macintosh Hierarchical File System.')
hrFSMFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 8))
if mibBuilder.loadTexts:
    hrFSMFS.setDescription('The file system type identifier used for the\n           Macintosh File System.')
hrFSNTFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 9))
if mibBuilder.loadTexts:
    hrFSNTFS.setDescription('The file system type identifier used for the\n           Windows NT File System.')
hrFSVNode = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 10))
if mibBuilder.loadTexts:
    hrFSVNode.setDescription('The file system type identifier used for the\n           VNode File System.')
hrFSJournaled = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 11))
if mibBuilder.loadTexts:
    hrFSJournaled.setDescription('The file system type identifier used for the\n           Journaled File System.')
hrFSiso9660 = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 12))
if mibBuilder.loadTexts:
    hrFSiso9660.setDescription("The file system type identifier used for the\n           ISO 9660 File System for CD's.")
hrFSRockRidge = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 13))
if mibBuilder.loadTexts:
    hrFSRockRidge.setDescription("The file system type identifier used for the\n           RockRidge File System for CD's.")
hrFSNFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 14))
if mibBuilder.loadTexts:
    hrFSNFS.setDescription('The file system type identifier used for the\n           NFS File System.')
hrFSNetware = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 15))
if mibBuilder.loadTexts:
    hrFSNetware.setDescription('The file system type identifier used for the\n           Netware File System.')
hrFSAFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 16))
if mibBuilder.loadTexts:
    hrFSAFS.setDescription('The file system type identifier used for the\n           Andrew File System.')
hrFSDFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 17))
if mibBuilder.loadTexts:
    hrFSDFS.setDescription('The file system type identifier used for the\n           OSF DCE Distributed File System.')
hrFSAppleshare = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 18))
if mibBuilder.loadTexts:
    hrFSAppleshare.setDescription('The file system type identifier used for the\n           AppleShare File System.')
hrFSRFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 19))
if mibBuilder.loadTexts:
    hrFSRFS.setDescription('The file system type identifier used for the\n           RFS File System.')
hrFSDGCFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 20))
if mibBuilder.loadTexts:
    hrFSDGCFS.setDescription('The file system type identifier used for the\n           Data General DGCFS.')
hrFSBFS = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 21))
if mibBuilder.loadTexts:
    hrFSBFS.setDescription('The file system type identifier used for the\n           SVR4 Boot File System.')
hrFSFAT32 = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 22))
if mibBuilder.loadTexts:
    hrFSFAT32.setDescription('The file system type identifier used for the\n           Windows FAT32 File System.')
hrFSLinuxExt2 = ObjectIdentity((1, 3, 6, 1, 2, 1, 25, 3, 9, 23))
if mibBuilder.loadTexts:
    hrFSLinuxExt2.setDescription('The file system type identifier used for the\n           Linux EXT2 File System.')
mibBuilder.exportSymbols('HOST-RESOURCES-TYPES', hrDeviceParallelPort=hrDeviceParallelPort, hrFSVNode=hrFSVNode, hrFSBFS=hrFSBFS, hrStorageRam=hrStorageRam, hrFSSys5FS=hrFSSys5FS, PYSNMP_MODULE_ID=hostResourcesTypesModule, hrDeviceOther=hrDeviceOther, hrFSTypes=hrFSTypes, hrDeviceCoprocessor=hrDeviceCoprocessor, hrDeviceNonVolatileMemory=hrDeviceNonVolatileMemory, hrFSNetware=hrFSNetware, hrFSBerkeleyFFS=hrFSBerkeleyFFS, hrFSMFS=hrFSMFS, hrStorageFloppyDisk=hrStorageFloppyDisk, hrDevicePointing=hrDevicePointing, hrFSHPFS=hrFSHPFS, hrFSUnknown=hrFSUnknown, hrStorageOther=hrStorageOther, hrDeviceVideo=hrDeviceVideo, hrFSDGCFS=hrFSDGCFS, hrStorageRamDisk=hrStorageRamDisk, hrDeviceVolatileMemory=hrDeviceVolatileMemory, hostResourcesTypesModule=hostResourcesTypesModule, hrDeviceTape=hrDeviceTape, hrFSFAT32=hrFSFAT32, hrDeviceNetwork=hrDeviceNetwork, hrFSLinuxExt2=hrFSLinuxExt2, hrStorageTypes=hrStorageTypes, hrFSRockRidge=hrFSRockRidge, hrStorageRemovableDisk=hrStorageRemovableDisk, hrDevicePrinter=hrDevicePrinter, hrDeviceSerialPort=hrDeviceSerialPort, hrDeviceClock=hrDeviceClock, hrDeviceProcessor=hrDeviceProcessor, hrStorageVirtualMemory=hrStorageVirtualMemory, hrDeviceAudio=hrDeviceAudio, hrDeviceUnknown=hrDeviceUnknown, hrStorageCompactDisc=hrStorageCompactDisc, hrStorageFlashMemory=hrStorageFlashMemory, hrFSHFS=hrFSHFS, hrDeviceModem=hrDeviceModem, hrFSFat=hrFSFat, hrFSiso9660=hrFSiso9660, hrFSOther=hrFSOther, hrFSAFS=hrFSAFS, hrFSDFS=hrFSDFS, hrDeviceDiskStorage=hrDeviceDiskStorage, hrDeviceTypes=hrDeviceTypes, hrFSRFS=hrFSRFS, hrFSNFS=hrFSNFS, hrDeviceKeyboard=hrDeviceKeyboard, hrStorageNetworkDisk=hrStorageNetworkDisk, hrFSJournaled=hrFSJournaled, hrFSAppleshare=hrFSAppleshare, hrFSNTFS=hrFSNTFS, hrStorageFixedDisk=hrStorageFixedDisk)
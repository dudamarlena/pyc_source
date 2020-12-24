# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pysnmp/smi/mibs/SNMP-USM-AES-MIB.py
# Compiled at: 2019-08-18 17:24:05
(OctetString, Integer, ObjectIdentifier) = mibBuilder.importSymbols('ASN1', 'OctetString', 'Integer', 'ObjectIdentifier')
(NamedValues,) = mibBuilder.importSymbols('ASN1-ENUMERATION', 'NamedValues')
(ValueSizeConstraint, ConstraintsUnion, SingleValueConstraint, ValueRangeConstraint, ConstraintsIntersection) = mibBuilder.importSymbols('ASN1-REFINEMENT', 'ValueSizeConstraint', 'ConstraintsUnion', 'SingleValueConstraint', 'ValueRangeConstraint', 'ConstraintsIntersection')
(snmpPrivProtocols,) = mibBuilder.importSymbols('SNMP-FRAMEWORK-MIB', 'snmpPrivProtocols')
(NotificationGroup, ModuleCompliance) = mibBuilder.importSymbols('SNMPv2-CONF', 'NotificationGroup', 'ModuleCompliance')
(Counter32, iso, ModuleIdentity, IpAddress, MibIdentifier, Integer32, TimeTicks, snmpModules, Bits, Gauge32, NotificationType, ObjectIdentity, Unsigned32, MibScalar, MibTable, MibTableRow, MibTableColumn, Counter64) = mibBuilder.importSymbols('SNMPv2-SMI', 'Counter32', 'iso', 'ModuleIdentity', 'IpAddress', 'MibIdentifier', 'Integer32', 'TimeTicks', 'snmpModules', 'Bits', 'Gauge32', 'NotificationType', 'ObjectIdentity', 'Unsigned32', 'MibScalar', 'MibTable', 'MibTableRow', 'MibTableColumn', 'Counter64')
(DisplayString, TextualConvention) = mibBuilder.importSymbols('SNMPv2-TC', 'DisplayString', 'TextualConvention')
snmpUsmAesMIB = ModuleIdentity((1, 3, 6, 1, 6, 3, 20))
if mibBuilder.loadTexts:
    snmpUsmAesMIB.setRevisions(('2004-06-14 00:00', ))
if mibBuilder.loadTexts:
    snmpUsmAesMIB.setLastUpdated('200406140000Z')
if mibBuilder.loadTexts:
    snmpUsmAesMIB.setOrganization('IETF')
if mibBuilder.loadTexts:
    snmpUsmAesMIB.setContactInfo('Uri Blumenthal Lucent Technologies / Bell Labs 67 Whippany Rd. 14D-318 Whippany, NJ 07981, USA 973-386-2163 uri@bell-labs.com Fabio Maino Andiamo Systems, Inc. 375 East Tasman Drive San Jose, CA 95134, USA 408-853-7530 fmaino@andiamo.com Keith McCloghrie Cisco Systems, Inc. 170 West Tasman Drive San Jose, CA 95134-1706, USA 408-526-5260 kzm@cisco.com')
if mibBuilder.loadTexts:
    snmpUsmAesMIB.setDescription("Definitions of Object Identities needed for the use of AES by SNMP's User-based Security Model. Copyright (C) The Internet Society (2004). This version of this MIB module is part of RFC 3826; see the RFC itself for full legal notices. Supplementary information may be available on http://www.ietf.org/copyrights/ianamib.html.")
usmAesCfb128Protocol = ObjectIdentity((1, 3, 6, 1, 6, 3, 10, 1, 2, 4))
if mibBuilder.loadTexts:
    usmAesCfb128Protocol.setStatus('current')
if mibBuilder.loadTexts:
    usmAesCfb128Protocol.setDescription('The CFB128-AES-128 Privacy Protocol.')
if mibBuilder.loadTexts:
    usmAesCfb128Protocol.setReference('- Specification for the ADVANCED ENCRYPTION STANDARD. Federal Information Processing Standard (FIPS) Publication 197. (November 2001). - Dworkin, M., NIST Recommendation for Block Cipher Modes of Operation, Methods and Techniques. NIST Special Publication 800-38A (December 2001). ')
mibBuilder.exportSymbols('SNMP-USM-AES-MIB', usmAesCfb128Protocol=usmAesCfb128Protocol, snmpUsmAesMIB=snmpUsmAesMIB, PYSNMP_MODULE_ID=snmpUsmAesMIB)
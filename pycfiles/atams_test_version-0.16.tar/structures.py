# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIGPC4\Desktop\atamsPackage\build\lib\atams\structures.py
# Compiled at: 2018-09-26 05:31:18
"""
---------------------------------------------------

        File name: structures.py

---------------------------------------------------
        Description:   

---------------------------------------------------     
        Package     : 
        Version     : 
        Language    : Python
        Authors         : 

Revision History:

Version         Created                         Modification
-----------------------------------------------------------------
"""
from ctypes import *

class UPLINK(Structure):
    _fields_ = [
     (
      'strPol', c_char * 16), ('dModemFrequency', c_double), ('dRfFrequency', c_double), ('dSatLo', c_double), ('dRate', c_double), ('dPower', c_double)]


class DOWNLINK(Structure):
    _fields_ = [
     (
      'strPol', c_char * 16), ('dModemFrequency', c_double), ('dRfFrequency', c_double), ('dSatLo', c_double), ('dRate', c_double)]


class SATELLITE(Structure):
    _fields_ = [
     (
      'Uplink', UPLINK), ('Downlink', DOWNLINK), ('strID', c_char * 16), ('strBeamID', c_char * 8), ('iBeam', c_int)]


class CHANNELSITE(Structure):
    _fields_ = [
     (
      'strSiteType', c_char * 16), ('strSite', c_char * 16), ('dLatitude', c_double), ('dLongitude', c_double), ('dAltitude', c_double)]


class CHANNEL(Structure):
    _fields_ = [
     (
      'Satellite', SATELLITE), ('PeerSite', CHANNELSITE), ('strID', c_char * 16), ('strRegion', c_char * 16)]


class CHANNELPLAN(Structure):
    _fields_ = [
     (
      'strError', c_char * 128), ('Channel', CHANNEL), ('LocalSite', CHANNELSITE), ('dwEffectivity', c_ulong), ('ret', c_int)]


class HANDOVER(Structure):
    _fields_ = [
     (
      'strTime', c_char * 20), ('strRegion', c_char * 16), ('strBeam', c_char * 8), ('dwTime', c_ulong), ('dwRealTime', c_ulong)]


class TRACK(Structure):
    _fields_ = [
     (
      'Handover', HANDOVER), ('strPrePassTime', c_char * 20), ('strStartTime', c_char * 20), ('strEndTime', c_char * 20), ('strSatelliteID', c_char * 16), ('dwPrePassTime', c_ulong),
     (
      'dwRealPrePassTime', c_ulong), ('dwStartTime', c_ulong), ('dwEndTime', c_ulong)]


class SCHEDULE(Structure):
    _fields_ = [
     (
      'Track', TRACK * 32), ('strError', c_char * 128), ('strPeriod', c_char * 16), ('strAction', c_char * 8), ('iPeriod', c_uint), ('iTrackIndex', c_int), ('iSatelliteCount', c_int),
     (
      'ret', c_int)]


class EPHEMERISARRAY(Structure):
    _fields_ = [
     (
      'strLine1', c_char * 128), ('strLine2', c_char * 128), ('strSatelliteID', c_char * 16)]


class EPHEMERIS(Structure):
    _fields_ = [
     (
      'EphemerisArray', EPHEMERISARRAY * 32), ('strError', c_char * 128), ('iSatelliteCount', c_int), ('ret', c_int)]


class SPACECRAFTARRAY(Structure):
    _fields_ = [
     (
      'strSatelliteID', c_char * 16), ('strBeaconFreqPri', c_char * 16), ('strBeaconFreqSec', c_char * 16), ('strBeaconPolPri', c_char * 16), ('strBeaconPolSec', c_char * 16),
     (
      'dBeaconFreqPri', c_double), ('dBeaconFreqSec', c_double)]


class SPACECRAFT(Structure):
    _fields_ = [
     (
      'SpacecraftArray', SPACECRAFTARRAY * 32), ('strError', c_char * 128), ('iSatelliteCount', c_int), ('ret', c_int)]


class STRUCTSATELLITE(Structure):
    _fields_ = [
     (
      'ro', c_double * 3), ('vo', c_double * 3), ('dLatitude', c_double), ('dLongitude', c_double), ('dAltitude', c_double), ('gsrt', c_double)]


MP_TABLE = ' CREATE TABLE IF NOT EXISTS MonitorParams (\n\t\t\t\t\tid integer PRIMARY KEY,\n\t\t\t\t\tstrUTCTime string NOT NULL,\n\t\t\t\t\tstrATAMSver string NOT NULL,\n\t\t\t\t\tstrATAMSStatus string NOT NULL,\n\t\t\t\t\tdLatitude float NOT NULL,\n\t\t\t\t\tdLongitude float NOT NULL,\n\t\t\t\t\tstrTrackingMethod string NOT NULL,\n\t\t\t\t\tstrCurrentSatID string NOT NULL,\n\t\t\t\t\tstrNextSatID string NOT NULL,\n\t\t\t\t\tstrHandoverTime string NOT NULL,\n\t\t\t\t\tiHandoverCounter int NOT NULL,\n\t\t\t\t\tdFrequency float NOT NULL,\n\t\t\t\t\tdBandwidth float NOT NULL,\n\t\t\t\t\tstrPol string NOT NULL,\n\t\t\t\t\tstrRxStatus string NOT NULL,\n\t\t\t\t\tbModManStatus bool NOT NULL,\n\t\t\t\t\tbAntennaStatus bool NOT NULL\n\t\t\t\t); '
MP_INSERT = ' INSERT INTO MonitorParams (strUTCTime, strATAMSver, strATAMSStatus, dLatitude, dLongitude, \n\t\t\t\t\t\t\t\t\t\t\tstrTrackingMethod, strCurrentSatID, strNextSatID, strHandoverTime, iHandoverCounter,\n\t\t\t\t\t\t\t\t\t\t\t\tdFrequency, dBandwidth, strPol, strRxStatus, bModManStatus, bAntennaStatus)\n\t\t\t\t\t\tVALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) '
MP_DEFAULT_SET = (
 '00:00:00', '0.1', 0, 248, 'Running', 'MEO', 'O3B M001', 'O3B M002', '00:30:00', 0, 1270, 35, 'LHCP', 'UnLocked', False, False)
CONFIG_TABLE = ' CREATE TABLE IF NOT EXISTS ConfigParams (\n\t\t\t\t\tid integer PRIMARY KEY,\n\t\t\t\t\tiAPImsgfreq int NOT NULL,\n\t\t\t\t\tiAMIPmsgfreq int NOT NULL,\n\t\t\t\t\tbATAMSRestart bool NOT NULL,\n\t\t\t\t\tbATAMSGUIRestart bool NOT NULL,\n\t\t\t\t\tbModManAPIRestart bool NOT NULL,\n\t\t\t\t\tbModManAMIPRestart bool NOT NULL,\n\t\t\t\t\tbAntennaAMIPRestart bool NOT NULL\n\t\t\t\t); '
CONFIG_INSERT = ' INSERT INTO ConfigParams (iAPImsgfreq, iAMIPmsgfreq, bATAMSRestart, bATAMSGUIRestart, bModManAPIRestart,\n\t\t\t\t\t\t\t\t\t\t\t\tbModManAMIPRestart, bAntennaAMIPRestart)\n\t\t\t\t\t\tVALUES(?,?,?,?,?,?,?) '
CONFIG_DEFAULT_SET = (
 10, 1, False, False, False, False, False)
IP_TABLE = ' CREATE TABLE IF NOT EXISTS IPSettings (\n\t\t\t\t\tid integer PRIMARY KEY,\n\t\t\t\t\tNTPIP string NOT NULL,\n\t\t\t\t\tModManIP string NOT NULL,\n\t\t\t\t\tAntennaIP string NOT NULL,\n\t\t\t\t\tModManAMIPPort string NOT NULL,\n\t\t\t\t\tAntennaAMIPPort string NOT NULL,\n\t\t\t\t\tModManAPIPort string NOT NULL\n\t\t\t\t); '
IP_INSERT = ' INSERT INTO IPSettings (NTPIP, ModManIP, AntennaIP, ModManAMIPPort, AntennaAMIPPort, ModManAPIPort)\n\t\t\t\t\t\tVALUES(?,?,?,?,?,?) '
IP_DEFAULT_SET = ('pool.ntp.org', '192.168.1.70', '192.168.1.80', 6200, 6200, 6300)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\SIGPC4\Desktop\atamsPackage\build\lib\atams\ephemerisvalidity.py
# Compiled at: 2018-09-26 05:36:22
"""
---------------------------------------------------

        File name: ephemerisvalidity.py

---------------------------------------------------
        Description:   Validates Ephemeris file by reading TLE lines
                                   If no TLEs found, returns error

---------------------------------------------------     
        Package     : atams
        Version     : 0.1
        Language    : Python
        Authors         : 

Revision History:

Version         Created                         Modification
-----------------------------------------------------------------

"""
from structures import *
import time
from datetime import datetime, timedelta
import os

def EphemerisValidity(EphemerisFilepath):
    i = n = m = 0
    bline1 = True
    bline2 = bcheck = False
    ChksumValid1 = ChksumValid2 = FutureValid = True
    EphemerisFilepath = os.path.join(EphemerisFilepath, 'ephemeris')
    fp = open(EphemerisFilepath, 'r')
    fp1 = fp.readlines()
    pattern = '%Y-%m-%d %H:%M:%S.%f'
    for line in fp1:
        if 'O3B' in line:
            data = ''
            data = data + line.strip()
            strSatelliteID = data
            i = i + 1
        if len(line) >= 69 and bline1:
            n = n + 1
            data = ''
            data = data + line.strip()
            bcheck = True
            bline2 = False
            strLine1 = data
            Time = strLine1[18:32]
            year = 2000 + int(Time[0:2])
            days = float(Time[2:])
            EphTime = datetime(year, 1, 1) + timedelta(days - 1)
            EphTime = EphTime.strftime(pattern)
            EphSec = int(time.mktime(time.strptime(str(EphTime), pattern)))
            CurEpoch = time.time()
            if CurEpoch < EphSec:
                FutureValid = False
                break
            else:
                FutureValid = True
            chksum = checksum(strLine1)
            if chksum != int(strLine1[68]):
                ChksumValid1 = False
                break
            else:
                ChksumValid1 = True
        if len(line) >= 69 and bline2:
            m = m + 1
            data = ''
            data = data + line.strip()
            bline1 = True
            bcheck = False
            strLine2 = data
            chksum = checksum(strLine2)
            if chksum != int(strLine2[68]):
                ChksumValid2 = False
                break
            else:
                ChksumValid2 = True
        if bcheck:
            bline2 = True
            bline1 = False

    iSatelliteCount = i
    fp.close()
    if iSatelliteCount < 1:
        Output = 'No TLEs found in ephemeris file'
        Valid = False
        return [
         Valid, Output]
    else:
        if ChksumValid1 == False:
            Output = 'Inavalid checksum in TLE Line-1:%d -file rejected' % n
            Valid = False
            return [
             Valid, Output]
        if ChksumValid2 == False:
            Output = 'Inavalid checksum in TLE Line-2:%d -file rejected' % m
            Valid = False
            return [
             Valid, Output]
        if FutureValid == False:
            Output = 'Invalid (future) Epoch Time in TLE Line-1:%d -file rejected' % n
            Valid = False
            return [
             Valid, Output]
        Valid = True
        Output = True
        return [Valid, Output]


def checksum(line):
    cksum = 0
    for i in range(68):
        c = line[i]
        if c == ' ' or c == '.' or c == '+' or c.isalpha():
            continue
        elif c == '-':
            cksum = cksum + 1
        else:
            cksum = cksum + int(c)

    cksum %= 10
    return cksum
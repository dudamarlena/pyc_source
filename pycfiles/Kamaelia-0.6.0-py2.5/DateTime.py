# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/Kamaelia/Support/DVB/DateTime.py
# Compiled at: 2008-10-19 12:19:52
"""Date and time parsing for DVB PSI tables
"""

def parseMJD(MJD):
    """Parse 16 bit unsigned int containing Modified Julian Date, as per DVB-SI spec
    returning year,month,day"""
    YY = int((MJD - 15078.2) / 365.25)
    MM = int((MJD - 14956.1 - int(YY * 365.25)) / 30.6001)
    D = MJD - 14956 - int(YY * 365.25) - int(MM * 30.6001)
    K = 0
    if MM == 14 or MM == 15:
        K = 1
    return (1900 + YY + K, MM - 1 - K * 12, D)


def unBCD(byte):
    return (byte >> 4) * 10 + (byte & 15)
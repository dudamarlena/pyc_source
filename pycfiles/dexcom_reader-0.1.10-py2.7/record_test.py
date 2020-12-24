# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dexcom_reader/record_test.py
# Compiled at: 2016-05-28 14:54:23
import readdata
dd = readdata.Dexcom.FindDevice()
dr = readdata.Dexcom(dd)
meter_records = dr.ReadRecords('METER_DATA')
print 'First Meter Record = '
print meter_records[0]
print 'Last Meter Record ='
print meter_records[(-1)]
insertion_records = dr.ReadRecords('INSERTION_TIME')
print 'First Insertion Record = '
print insertion_records[0]
print 'Last Insertion Record = '
print insertion_records[(-1)]
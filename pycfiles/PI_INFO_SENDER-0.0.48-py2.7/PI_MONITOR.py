# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-armv7l/egg/PI_INFO_SENDER/PI_MONITOR.py
# Compiled at: 2016-08-31 03:15:19
import paho.mqtt.client as mqtt, time, os, json, sys

def getCPUtemp():
    cputemp_rawdata = os.popen('sudo vcgencmd measure_temp').readline()
    cputemp = cputemp_rawdata.replace('temp=', '').replace("'C\n", '')
    cputemp = '%.2f' % float(cputemp)
    return cputemp


def getCPUuse():
    cpu_use_rawdata = os.popen('sudo mpstat -P ALL 1 1').read()
    cpu_use_rawdata = cpu_use_rawdata.split('\n\n', 2)[1]
    cpu_use_rawdata = cpu_use_rawdata.split('\n', 1)[1]
    line = len(cpu_use_rawdata.split('\n'))
    cpu_usage = range(0, line)
    for i in range(0, line):
        row = cpu_use_rawdata.split('\n')[i]
        if i != 0:
            cpu_usage[i] = '%.2f' % (float(row.split()[2]) / 4)
        else:
            cpu_usage[i] = '%.2f' % float(row.split()[2])
        i = i + 1

    return cpu_usage


def getRAMinfo():
    raminfo_rawdata = os.popen('sudo free').read()
    raminfo_rawdata = raminfo_rawdata.split('\n')
    raminfo = range(0, 3)
    raminfo[0] = raminfo_rawdata[1].split()[1]
    raminfo[0] = '%.2f' % (float(raminfo[0]) / 1024.0)
    for i in range(1, 3):
        raminfo[i] = '%.2f' % (float(raminfo_rawdata[2].split()[(i + 1)]) / 1024.0)

    return raminfo


def getDISKinfo():
    diskinfo_rawdata = os.popen('sudo df -h /').read()
    diskinfo_rawdata = diskinfo_rawdata.split('\n')[1]
    diskinfo = range(0, 4)
    for i in range(0, 4):
        diskinfo[i] = diskinfo_rawdata.split()[(i + 1)]
        diskinfo[i] = diskinfo[i].replace('G', '')
        diskinfo[i] = diskinfo[i].replace('%', '')
        diskinfo[i] = '%.2f' % float(diskinfo[i])

    return diskinfo


def SysstatInstallaion():
    sysstat_rawdata = os.popen('sudo dpkg -l | grep sysstat').read()
    if 'sysstat' not in sysstat_rawdata:
        os.system('sudo dpkg -i sysstat.deb')
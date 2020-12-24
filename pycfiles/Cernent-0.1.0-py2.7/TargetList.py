# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/reports/TargetList.py
# Compiled at: 2012-04-20 03:24:19


def getExtension():
    return '.txt'


def getName():
    return __file__.split('.')[0]


def getDescription():
    return 'Prints the alphanumeric sorted list of targets in the scan.'


def getResult(rf):
    rpt = rf.rpts[0]
    msg = rf.getStatusMsg('List of targets scanned')
    for target in sorted(rpt.targets, key=lambda t: t.name):
        msg += target.name + '\n'

    return msg


def writeResult(rf, outputPath):
    path = outputPath + getExtension()
    rf.msWrite(getResult(rf), path)
    return path
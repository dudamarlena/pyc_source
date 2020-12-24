# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
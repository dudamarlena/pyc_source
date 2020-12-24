# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/reports/Credentialed.py
# Compiled at: 2012-04-20 03:22:55


def getExtension():
    return '.txt'


def getName():
    return __file__.split('.')[0]


def getDescription():
    return 'Reports whether or not a host was scanned using credentials or not. Printing the credentials used for the scan if appropriate'


def getResult(rf):
    rpt = rf.rpts[0]
    creds = []
    uncreds = []
    msg = ''
    for target in rpt.targets:
        if target.credentialed:
            creds.append(target)
        else:
            uncreds.append(target)

    msg += rf.getStatusMsg('Credentialed Scan')
    for target in creds:
        msg += target.name + '\n'
        for cred in target.credentialed:
            msg += '\t%s\n' % cred

    msg += rf.getStatusMsg('Uncredentialed Scan')
    for target in uncreds:
        msg += target.name + '\n'

    return msg


def writeResult(rf, outputPath):
    path = outputPath + getExtension()
    rf.msWrite(getResult(rf), path)
    return path
# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/reports/RebootRequired.py
# Compiled at: 2012-04-20 03:23:07
import re

def getExtension():
    return '.txt'


def getName():
    return __file__.split('.')[0]


def getDescription():
    return 'Report contains a list of devices that require a reboot from patches. This is mostly a windows reboot check.'


def getResult(rf):
    rpt = rf.rpts[0]
    hosts = []
    msg = ''
    for target in rpt.targets:
        for vuln in target.vulns:
            if re.search('reboot', vuln.plugin_name, re.IGNORECASE):
                hosts.append([target, vuln.plugin_name])
                msg += '%s (%s) -> %s' % (target.get_name(), (', ').join(target.get_ips()), vuln.plugin_name)

    return msg


def writeResult(rf, outputPath):
    path = outputPath + getExtension()
    rf.msWrite(getResult(rf), path)
    return path
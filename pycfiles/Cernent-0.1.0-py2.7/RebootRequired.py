# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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
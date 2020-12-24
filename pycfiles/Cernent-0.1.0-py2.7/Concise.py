# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/reports/Concise.py
# Compiled at: 2012-04-20 03:23:31


def getExtension():
    return '.txt'


def getName():
    return __file__.split('.')[0]


def getDescription():
    return 'Reports the concise information needed to resolve vulnerabilities'


def getResult(rf):
    rpt = rf.rpts[0]
    msg = rf.getStatusMsg(rpt.name, 50)
    msg += 'Date: %s\n' % rpt.scan_start
    msg += 'Hosts: %s\n' % rpt.stats['targetsCount']
    msg += 'Critical: %s\n' % rpt.stats['critCount']
    msg += 'Highs: %s\n' % rpt.stats['highCount']
    for target in rpt.targets:
        if target.criticals or target.highs or target.mediums:
            msg += rf.getStatusMsg(target.get_name(), 50)
            if target.criticals:
                msg += rf.getStatusMsg('Criticals', 15, '-')
                for plugin_name in target.criticals:
                    msg += plugin_name + '\n'

            if target.highs:
                msg += rf.getStatusMsg('Highs', 15, '-')
                for plugin_name in target.highs:
                    msg += plugin_name + '\n'

            if target.mediums:
                msg += rf.getStatusMsg('Mediums', 15, '-')
                for plugin_name in target.mediums:
                    msg += plugin_name + '\n'

            msg += '\n'

    return msg


def writeResult(rf, outputPath):
    path = outputPath + getExtension()
    rf.msWrite(getResult(rf), path)
    return path
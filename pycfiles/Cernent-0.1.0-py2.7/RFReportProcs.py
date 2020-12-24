# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ReportFramework/RFReportProcs.py
# Compiled at: 2012-04-22 01:12:48


def init(rpt):
    rpt.stats = {}
    rpt.host = {}
    rpt.reboots = []
    rpt.stats['targetsCount'] = len(rpt.targets)
    pers = [
     ('critPer', 'critCount'),
     ('highPer', 'highCount'),
     ('mediumPer', 'mediumCount'),
     ('lowPer', 'lowCount')]
    for per, count in pers:
        rpt.stats[per] = []

    intVars = ['pubExploitCount', 'metasploitCount', 'lowCount', 'mediumCount', 'highCount', 'critCount']
    for var in intVars:
        rpt.stats[var] = 0


def popStats(rpt):
    avgVars = [
     ('avgCriticals', 'critPer'),
     ('avgHighs', 'highPer'),
     ('avgMediums', 'mediumPer'),
     ('avgLows', 'lowPer')]
    if rpt.stats['targetsCount']:
        for avg, per in avgVars:
            rpt.stats[avg] = sum(rpt.stats[per]) / rpt.stats['targetsCount']
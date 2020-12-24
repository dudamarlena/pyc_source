# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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
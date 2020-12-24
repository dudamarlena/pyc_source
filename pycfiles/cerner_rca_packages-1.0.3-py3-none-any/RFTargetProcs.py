# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.6-intel/egg/ReportFramework/RFTargetProcs.py
# Compiled at: 2012-04-20 01:26:12


def init(rpt, tgt):
    tgt.stats = {}
    tgt.reboot = False
    tgt.criticals, tgt.highs, tgt.mediums, tgt.lows = ([], [], [], [])
    tgt.credentialed = []
    intVars = [
     'pubExploitCount', 'metasploitCount', 'lowCount', 'mediumCount', 'highCount', 'critCount']
    for var in intVars:
        tgt.stats[var] = 0


def default(rpt, tgt):
    rpt.host[tgt.get_name()] = tgt
    pers = [
     ('critPer', 'critCount'),
     ('highPer', 'highCount'),
     ('mediumPer', 'mediumCount'),
     ('lowPer', 'lowCount')]
    for per, count in pers:
        rpt.stats[per].append(tgt.stats[count])

    tgt.criticals.sort()
    tgt.highs.sort()
    tgt.mediums.sort()
    tgt.lows.sort()
    tgt.criticalSet = set(tgt.criticals)
    tgt.highSet = set(tgt.highs)
    tgt.mediumSet = set(tgt.mediums)
    tgt.lowSet = set(tgt.lows)
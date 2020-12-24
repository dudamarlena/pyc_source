# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/cf/userstatus.py
# Compiled at: 2019-07-09 05:11:54
# Size of source mod 2**32: 1023 bytes
from cf.util import *
from cf.classes import *
from prettytable import PrettyTable as PT
import pydoc

def userstatus(res):
    res = res['result']
    s = []
    for r in res:
        s.append(Submission(r))

    pt = PT()
    fn = ['Problem ID', 'Problem Name', 'Points', 'Language', 'Verdict', 'TestSet', 'Passed Tests', 'Time(ms)', 'Memory(bytes)']
    for i in range(len(fn)):
        fn[i] = get_colored(fn[i], 'magenta')

    pt.field_names = fn
    for i in s:
        pid = str(i.problem.contestId) + str(i.problem.index)
        pname = str(i.problem.name)
        points = str(i.problem.points)
        lang = str(i.programmingLanguage)
        verd = str(i.verdict)
        ts = str(i.testset)
        ptest = str(i.passedTestCount)
        time = str(i.timeConsumedMillis)
        mem = str(i.memoryConsumedBytes)
        lis = [pid, pname, points, lang, verd, ts, ptest, time, mem]
        for j in range(len(lis)):
            lis[j] = get_colored(lis[j], 'cyan')

        pt.add_row(lis)

    pydoc.pager(pt.get_string())
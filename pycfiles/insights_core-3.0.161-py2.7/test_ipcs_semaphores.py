# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/combiners/tests/test_ipcs_semaphores.py
# Compiled at: 2019-05-16 13:41:33
from insights.parsers.ipcs import IpcsSI, IpcsS
from insights.parsers.ps import PsAuxcww
from insights.combiners import ipcs_semaphores
from insights.combiners.ipcs_semaphores import IpcsSemaphores
from insights.tests import context_wrap
import doctest
PsAuxcww_OUT = ('\nUSER       PID %CPU %MEM    VSZ   RSS TTY      STAT START   TIME COMMAND\nroot         1  0.0  0.0  19356  1544 ?        Ss   May31   0:01 init\nroot      6152  0.0  0.0      0     0 ?        S    May31   0:29 kondemand/0\nroot      2265  0.0  0.0  18244   668 ?        Ss   May31   0:05 irqbalance\n').strip()
IPCS_S = ('\n------ Semaphore Arrays --------\nkey        semid      owner      perms      nsems\n0x00000000 557056     apache     600        4\n0x00000000 655371     apache     600        1\n0x0052e2c1 65536      postgres   600        8\n0x00000000 622502     apache     600        1\n0x00000000 622602     apache     600        1\n0x00000000 688140     apache     600        1\n').strip()
IPCS_S_I_1 = '\nSemaphore Array semid=557056\nuid=500  gid=501     cuid=500    cgid=501\nmode=0600, access_perms=0600\nnsems = 4\notime = Sun May 12 14:44:53 2013\nctime = Wed May  8 22:12:15 2013\nsemnum     value      ncount     zcount     pid\n0          1          0          0          0\n1          1          0          0          0\n4          1          0          0          0\n5          1          0          0          0\n'
IPCS_S_I_2 = '\nSemaphore Array semid=65536\nuid=500  gid=501     cuid=500    cgid=501\nmode=0600, access_perms=0600\nnsems = 8\notime = Sun May 12 14:44:53 2013\nctime = Wed May  8 22:12:15 2013\nsemnum     value      ncount     zcount     pid\n0          1          0          0          0\n1          1          0          0          0\n0          1          0          0          6151\n3          1          0          0          2265\n4          1          0          0          0\n5          1          0          0          0\n0          0          7          0          6152\n7          1          0          0          4390\n\n'
IPCS_S_I_3 = '\nSemaphore Array semid=622502\nuid=48   gid=48  cuid=0  cgid=0\nmode=0600, access_perms=0600\nnsems = 1\notime = Wed Apr 12 15:41:03 2017\nctime = Wed Apr 12 15:41:03 2017\nsemnum     value      ncount     zcount     pid\n0          1          0          0          6151\n\n'
IPCS_S_I_4 = '\nSemaphore Array semid=622602\nuid=48   gid=48  cuid=0  cgid=0\nmode=0600, access_perms=0600\nnsems = 1\notime = Wed Apr 12 15:41:03 2017\nctime = Wed Apr 12 15:41:03 2017\nsemnum     value      ncount     zcount     pid\n0          1          0          0          6151\n\n'
IPCS_S_I_5 = '\nSemaphore Array semid=655371\nuid=48   gid=48  cuid=0  cgid=0\nmode=0600, access_perms=0600\nnsems = 1\notime = Not set\nctime = Wed Apr 12 15:41:03 2017\nsemnum     value      ncount     zcount     pid\n0          1          0          0          991\n\n'
IPCS_S_I_6 = ('\nSemaphore Array semid=688140\nuid=48   gid=48  cuid=0  cgid=0\nmode=0600, access_perms=0600\nnsems = 1\notime = Wed Apr 12 16:01:28 2017\nctime = Wed Apr 12 15:41:03 2017\nsemnum     value      ncount     zcount     pid\n0          0          7          0          6152\n').strip()

def test_ipcs_semaphores():
    sem1 = IpcsSI(context_wrap(IPCS_S_I_1))
    sem2 = IpcsSI(context_wrap(IPCS_S_I_2))
    sem3 = IpcsSI(context_wrap(IPCS_S_I_3))
    sem4 = IpcsSI(context_wrap(IPCS_S_I_4))
    sem5 = IpcsSI(context_wrap(IPCS_S_I_5))
    sem6 = IpcsSI(context_wrap(IPCS_S_I_6))
    sems = IpcsS(context_wrap(IPCS_S))
    ps = PsAuxcww(context_wrap(PsAuxcww_OUT))
    rst = IpcsSemaphores(sems, [sem1, sem2, sem3, sem4, sem5, sem6], ps)
    assert rst.get_sem('65536').pid_list == ['0', '2265', '4390', '6151', '6152']
    assert rst.count_of_all_sems() == 6
    assert rst.count_of_all_sems(owner='apache') == 5
    assert rst.count_of_orphan_sems() == 3
    assert rst.count_of_orphan_sems('postgres') == 0
    i = 0
    for sem in rst:
        i += 1

    assert i == rst.count_of_all_sems()
    assert rst.orphan_sems() == ['622502', '622602', '655371']
    assert rst.orphan_sems('apache') == ['622502', '622602', '655371']
    assert rst.orphan_sems('postgres') == []


def test_doc_examples():
    sem1 = IpcsSI(context_wrap(IPCS_S_I_1))
    sem2 = IpcsSI(context_wrap(IPCS_S_I_2))
    sem3 = IpcsSI(context_wrap(IPCS_S_I_3))
    sem4 = IpcsSI(context_wrap(IPCS_S_I_4))
    sem6 = IpcsSI(context_wrap(IPCS_S_I_6))
    sems = IpcsS(context_wrap(IPCS_S))
    ps = PsAuxcww(context_wrap(PsAuxcww_OUT))
    env = {'oph_sem': IpcsSemaphores(sems, [
                 sem1, sem2, sem3, sem4, sem6], ps)}
    failed, total = doctest.testmod(ipcs_semaphores, globs=env)
    assert failed == 0
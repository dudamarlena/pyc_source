# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tbent/Dropbox/projects/taskloaf/tests/conftest.py
# Compiled at: 2017-10-25 16:22:51
from mpi4py import MPI
import _pytest.runner

def pytest_runtest_protocol(item, nextitem):
    n_procs = getattr(item.function, 'n_procs', 1)
    rank = MPI.COMM_WORLD.Get_rank()
    size = MPI.COMM_WORLD.Get_size()
    if n_procs > size:
        print 'skipping ' + str(item.name) + ' because it needs ' + str(n_procs) + ' MPI procs'
        return True
    if rank >= n_procs:
        return True
    return _pytest.runner.pytest_runtest_protocol(item, nextitem)
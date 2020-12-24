# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/romainegele/Documents/Argonne/deephyper/build/lib/deephyper/search/nas/baselines/common/mpi_fork.py
# Compiled at: 2019-07-10 12:45:57
# Size of source mod 2**32: 667 bytes
import os, subprocess, sys

def mpi_fork(n, bind_to_core=False):
    """Re-launches the current script with workers
    Returns "parent" for original parent, "child" for MPI children
    """
    if n <= 1:
        return 'child'
    if os.getenv('IN_MPI') is None:
        env = os.environ.copy()
        env.update(MKL_NUM_THREADS='1',
          OMP_NUM_THREADS='1',
          IN_MPI='1')
        args = [
         'mpirun', '-np', str(n)]
        if bind_to_core:
            args += ['-bind-to', 'core']
        args += [sys.executable] + sys.argv
        subprocess.check_call(args, env=env)
        return 'parent'
    return 'child'
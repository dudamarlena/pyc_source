# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/pierre/github/spyking-circus/build/lib/circus/scripts/subtask.py
# Compiled at: 2019-11-21 10:47:18
# Size of source mod 2**32: 1680 bytes
"""
Script that launches a subtask. We cannot call functions directly from
the main spyking_circus script, since we want to start them with ``mpirun``.
"""
import sys, circus, logging
from circus.shared.messages import print_and_log
from circus.shared.mpi import test_mpi_ring
logger = logging.getLogger(__name__)

def main():
    argv = sys.argv
    if not len(sys.argv) in (6, 7, 8, 9):
        raise AssertionError('Incorrect number of arguments -- do not run this script manually, use "spyking-circus" instead')
    else:
        task = sys.argv[1]
        filename = sys.argv[2]
        nb_cpu = int(sys.argv[3])
        nb_gpu = int(sys.argv[4])
        test_mpi_ring(nb_cpu)
        use_gpu = sys.argv[5].lower() == 'true'
        print_and_log(['Launching subtask %s with params %s' % (task, sys.argv[2:])], 'debug', logger)
        if task == 'benchmarking':
            output = sys.argv[6]
            benchmark = sys.argv[7]
            if len(sys.argv) == 9:
                sim_same_elec = int(sys.argv[8])
                circus.launch(task, filename, nb_cpu, nb_gpu, use_gpu, output, benchmark, sim_same_elec=sim_same_elec)
            else:
                circus.launch(task, filename, nb_cpu, nb_gpu, use_gpu, output, benchmark)
        else:
            if task in ('converting', 'deconverting', 'merging'):
                extension = sys.argv[6]
                if extension == 'None':
                    extension = ''
                else:
                    if extension != '':
                        extension = '-' + extension
                circus.launch(task, filename, nb_cpu, nb_gpu, use_gpu, extension=extension)
            else:
                circus.launch(task, filename, nb_cpu, nb_gpu, use_gpu)
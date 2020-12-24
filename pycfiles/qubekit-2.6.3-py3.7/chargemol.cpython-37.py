# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/chargemol.py
# Compiled at: 2019-09-16 10:20:01
# Size of source mod 2**32: 2537 bytes
from QUBEKit.engines.base_engine import Engines
from QUBEKit.utils.decorators import for_all_methods, timer_logger
from QUBEKit.utils.helpers import append_to_log
from QUBEKit.utils.exceptions import ChargemolError
import os, subprocess as sp

@for_all_methods(timer_logger)
class Chargemol(Engines):

    def __init__(self, molecule):
        super().__init__(molecule)

    def generate_input(self, execute=True):
        """Given a DDEC version (from the defaults), this function writes the job file for chargemol and executes it."""
        if self.molecule.ddec_version != 6:
            if self.molecule.ddec_version != 3:
                append_to_log(message='Invalid or unsupported DDEC version given, running with default version 6.', msg_type='warning')
                self.molecule.ddec_version = 6
        with open('job_control.txt', 'w+') as (charge_file):
            charge_file.write(f"<input filename>\n{self.molecule.name}.wfx\n</input filename>")
            charge_file.write('\n\n<net charge>\n0.0\n</net charge>')
            charge_file.write('\n\n<periodicity along A, B and C vectors>\n.false.\n.false.\n.false.')
            charge_file.write('\n</periodicity along A, B and C vectors>')
            charge_file.write(f"\n\n<atomic densities directory complete path>\n{self.molecule.chargemol}/atomic_densities/")
            charge_file.write('\n</atomic densities directory complete path>')
            charge_file.write(f"\n\n<charge type>\nDDEC{self.molecule.ddec_version}\n</charge type>")
            charge_file.write('\n\n<compute BOs>\n.true.\n</compute BOs>')
        if execute:
            os.environ['OMP_NUM_THREADS'] = str(self.molecule.threads)
            with open('log.txt', 'w+') as (log):
                control_path = 'chargemol_FORTRAN_09_26_2017/compiled_binaries/linux/Chargemol_09_26_2017_linux_parallel job_control.txt'
                try:
                    sp.run((os.path.join(self.molecule.chargemol, control_path)), shell=True, stdout=log, stderr=log, check=True)
                except sp.CalledProcessError:
                    raise ChargemolError('Chargemol did not execute properly check the output file for details.')

                del os.environ['OMP_NUM_THREADS']
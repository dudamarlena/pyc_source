# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/gaussian.py
# Compiled at: 2019-09-20 10:07:20
# Size of source mod 2**32: 10400 bytes
from QUBEKit.engines.base_engine import Engines
from QUBEKit.utils import constants
from QUBEKit.utils.decorators import for_all_methods, timer_logger
from QUBEKit.utils.helpers import check_symmetry
import subprocess as sp, numpy as np

@for_all_methods(timer_logger)
class Gaussian(Engines):
    __doc__ = '\n    Writes and executes input files for Gaussian09.\n    Also used to extract Hessian matrices; optimised structures; frequencies; etc.\n    '

    def __init__(self, molecule):
        super().__init__(molecule)
        self.functional_dict = {'pbe':'PBEPBE', 
         'wb97x-d':'wB97XD',  'b3lyp-d3bj':'EmpiricalDispersion=GD3BJ B3LYP'}
        self.molecule.theory = self.functional_dict.get(self.molecule.theory.lower(), self.molecule.theory)
        self.convergence_dict = {'GAU':'', 
         'GAU_TIGHT':'tight', 
         'GAU_LOOSE':'loose', 
         'GAU_VERYTIGHT':'verytight'}

    def generate_input(self, input_type='input', optimise=False, hessian=False, energy=False, density=False, restart=False, execute='g09', red_mode=False):
        """
        Generates the relevant job file for Gaussian, then executes this job file.
        :param input_type: The set of coordinates in the molecule that should be used in the job
        :param optimise: Optimise the geometry of the molecule
        :param hessian: Calculate the hessian matrix
        :param energy: Calculate the single point energy
        :param density: Calculate the electron density
        :param restart: Restart from a check point file
        :param execute: Run the calculation after writing the input file
        :param red_mode: If we are doing a redundant mode optimisation this will only add the ModRedundant keyword,
        the rest of the input is hand wrote or handled by tdrive when required.
        :return: The exit status of the job if ran, True for normal false for not ran or error
        """
        if execute == 'g16':
            print('\nWe do not have the capability to test Gaussian 16; as a result, there may be some issues. Please let us know if any changes are needed through our Slack, or Github issues page.\n')
        with open(f"gj_{self.molecule.name}.com", 'w+') as (input_file):
            input_file.write(f"%Mem={self.molecule.memory}GB\n%NProcShared={self.molecule.threads}\n%Chk=lig\n")
            if self.molecule.excited_state:
                commands = f"# {self.molecule.theory}/{self.molecule.basis} "
                if self.molecule.use_pseudo:
                    commands += ' Pseudo=Read'
                commands += f" {self.molecule.excited_theory}=(Nstates={self.molecule.nstates}, Root={self.molecule.excited_root}) SCF=XQC "
            else:
                commands = f"# {self.molecule.theory}/{self.molecule.basis} SCF=XQC "
            if optimise:
                convergence = self.convergence_dict.get(self.molecule.convergence, '')
                if convergence:
                    convergence = f", {convergence}"
                if red_mode:
                    convergence = ', ModRedundant'
                commands += f"opt(MaxCycles={self.molecule.iterations}{convergence}) "
            if hessian:
                commands += 'freq '
            if energy:
                commands += 'SP '
            if density:
                commands += 'density=current OUTPUT=WFX '
                if self.molecule.solvent:
                    commands += 'SCRF=(IPCM,Read) '
            if restart:
                commands += 'geom=check'
            commands += f"\n\n{self.molecule.name}\n\n{self.molecule.charge} {self.molecule.multiplicity}\n"
            input_file.write(commands)
            if not restart:
                for i, atom in enumerate(self.molecule.coords[input_type]):
                    input_file.write(f"{self.molecule.atoms[i].atomic_symbol} {float(atom[0]): .10f} {float(atom[1]): .10f} {float(atom[2]): .10f}\n")

            if self.molecule.use_pseudo:
                input_file.write(f"\n{self.molecule.pseudo_potential_block}")
            if density:
                if self.molecule.solvent:
                    input_file.write('\n4.0 0.0004')
            if density:
                input_file.write(f"\n{self.molecule.name}.wfx")
            input_file.write('\n\n\n\n')
        if execute:
            with open('log.txt', 'w+') as (log):
                sp.run(f"{execute} < gj_{self.molecule.name}.com > gj_{self.molecule.name}.log", shell=True,
                  stdout=log,
                  stderr=log)
            return self.check_for_errors()
        return {'success':False,  'error':'Not run'}

    def check_for_errors(self):
        """
        Read the output file and check for normal termination and any errors.
        :return: A dictionary of the success status and any problems
        """
        with open(f"gj_{self.molecule.name}.log", 'r') as (log):
            for line in log:
                if 'Normal termination of Gaussian' in line:
                    return {'success': True}
                    if 'Problem with the distance matrix.' in line:
                        return {'success':False, 
                         'error':'Distance matrix'}
                    if 'Error termination in NtrErr' in line:
                        return {'success':False, 
                         'error':'FileIO'}
                    if '-- Number of steps exceeded' in line:
                        return {'success':False, 
                         'error':'Max iterations'}

            return {'success':False, 
             'error':'Unknown'}

    def hessian(self):
        """Extract the Hessian matrix from the Gaussian fchk file."""
        with open('formchck.log', 'w+') as (formlog):
            sp.run('formchk lig.chk lig.fchk', shell=True, stdout=formlog, stderr=formlog)
        with open('lig.fchk', 'r') as (fchk):
            lines = fchk.readlines()
            hessian_list = []
            start, end = (None, None)
            for count, line in enumerate(lines):
                if line.startswith('Cartesian Force Constants'):
                    start = count + 1
                if line.startswith('Nonadiabatic coupling'):
                    if end is None:
                        end = count
                if line.startswith('Dipole Moment') and end is None:
                    end = count

            if not start:
                if end:
                    raise EOFError('Cannot locate Hessian matrix in lig.fchk file.')
            conversion = constants.HA_TO_KCAL_P_MOL / constants.BOHR_TO_ANGS ** 2
            for line in lines[start:end]:
                hessian_list.extend([float(num) * conversion for num in line.strip('\n').split()])

        hess_size = 3 * len(self.molecule.atoms)
        hessian = np.zeros((hess_size, hess_size))
        m = 0
        for i in range(hess_size):
            for j in range(i + 1):
                hessian[(i, j)] = hessian_list[m]
                hessian[(j, i)] = hessian_list[m]
                m += 1

        check_symmetry(hessian)
        return hessian

    def optimised_structure(self):
        """
        Extract the optimised structure and energy from a fchk file
        :return molecule: The optimised array with the structure
        :return energy:  The SCF energy of the optimised structure
        """
        with open('formchck.log', 'w+') as (formlog):
            sp.run('formchk lig.chk lig.fchk', shell=True, stdout=formlog, stderr=formlog)
        with open('lig.fchk', 'r') as (fchk):
            lines = fchk.readlines()
        start, end, energy = (None, None, None)
        for count, line in enumerate(lines):
            if 'Current cartesian coordinates' in line:
                start = count + 1
            elif 'Number of symbols in' in line:
                if end is None:
                    end = count
            elif 'Int Atom Types' in line:
                if end is None:
                    end = count - 1
            elif 'Total Energy' in line:
                energy = float(line.split()[3])

        if any((val is None for val in [start, end, energy])):
            raise EOFError('Cannot locate optimised structure in file.')
        molecule = []
        for line in lines[start:end]:
            molecule.extend([float(coord) for coord in line.split()])

        molecule = np.array(molecule).reshape((len(self.molecule.atoms), 3)) * constants.BOHR_TO_ANGS
        return (
         molecule, energy)

    def all_modes(self):
        """Extract the frequencies from the Gaussian log file."""
        with open(f"gj_{self.molecule.name}.log", 'r') as (gj_log_file):
            lines = gj_log_file.readlines()
            freqs = []
            freq_positions = []
            for count, line in enumerate(lines):
                if line.startswith(' Frequencies'):
                    freq_positions.append(count)

            for pos in freq_positions:
                freqs.extend((float(num) for num in lines[pos].split()[2:]))

        return np.array(freqs)
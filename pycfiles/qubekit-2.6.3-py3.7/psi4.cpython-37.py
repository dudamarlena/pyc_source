# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/psi4.py
# Compiled at: 2019-09-16 10:20:01
# Size of source mod 2**32: 14281 bytes
from QUBEKit.engines.base_engine import Engines
from QUBEKit.utils import constants
from QUBEKit.utils.decorators import for_all_methods, timer_logger
from QUBEKit.utils.helpers import append_to_log, check_symmetry
from QUBEKit.utils.exceptions import Psi4Error
import subprocess as sp, numpy as np

@for_all_methods(timer_logger)
class PSI4(Engines):
    __doc__ = '\n    Writes and executes input files for psi4.\n    Also used to extract Hessian matrices; optimised structures; frequencies; etc.\n    '

    def __init__(self, molecule):
        super().__init__(molecule)
        self.functional_dict = {'pbepbe':'PBE', 
         'wb97xd':'wB97X-D'}
        self.molecule.theory = self.functional_dict.get(self.molecule.theory.lower(), self.molecule.theory)
        try:
            sp.run('psi4 -h', shell=True, check=True, stdout=(sp.PIPE))
        except sp.CalledProcessError:
            raise ModuleNotFoundError('PSI4 not working. Please ensure PSI4 is installed and can be called with the command: psi4')

        if self.molecule.geometric:
            try:
                sp.run('geometric-optimize -h', shell=True, check=True, stdout=(sp.PIPE))
            except sp.CalledProcessError:
                raise ModuleNotFoundError('Geometric not working. Please ensure geometric is installed and can be called with the command: geometric-optimize')

    def generate_input(self, input_type='input', optimise=False, hessian=False, density=False, energy=False, fchk=False, restart=False, execute=True):
        """
        Converts to psi4 input format to be run in psi4 without using geometric.
        :param input_type: The coordinate set of the molecule to be used
        :param optimise: Optimise the molecule to the desired convergence criterion within the iteration limit
        :param hessian: Calculate the hessian matrix
        :param density: Calculate the electron density
        :param energy: Calculate the single point energy of the molecule
        :param fchk: Write out a gaussian style Fchk file
        :param restart: Restart the calculation from a log point (required but unused to match g09's generate_input())
        :param execute: Run the desired Psi4 job
        :return: The completion status of the job True if successful False if not run or failed
        """
        setters = ''
        tasks = ''
        if energy:
            append_to_log('Writing psi4 energy calculation input')
            tasks += f"\nenergy('{self.molecule.theory}')"
        if optimise:
            append_to_log('Writing PSI4 optimisation input', 'minor')
            setters += f" g_convergence {self.molecule.convergence}\n GEOM_MAXITER {self.molecule.iterations}\n"
            tasks += f"\noptimize('{self.molecule.theory.lower()}')"
        if hessian:
            append_to_log('Writing PSI4 Hessian matrix calculation input', 'minor')
            setters += ' hessian_write on\n'
            tasks += f"\nenergy, wfn = frequency('{self.molecule.theory.lower()}', return_wfn=True)"
            tasks += '\nwfn.hessian().print_out()\n\n'
        if density:
            pass
        if fchk:
            append_to_log('Writing PSI4 input file to generate fchk file')
            tasks += f"\ngrad, wfn = gradient('{self.molecule.theory.lower()}', return_wfn=True)"
            tasks += '\nfchk_writer = psi4.core.FCHKWriter(wfn)'
            tasks += f'\nfchk_writer.write("{self.molecule.name}_psi4.fchk")\n'
        if self.molecule.solvent:
            pass
        setters += '}\n'
        if not execute:
            setters += f"set_num_threads({self.molecule.threads})\n"
        with open('input.dat', 'w+') as (input_file):
            input_file.write(f"memory {self.molecule.memory} GB\n\nmolecule {self.molecule.name} {{\n{self.molecule.charge} {self.molecule.multiplicity} \n")
            for i, atom in enumerate(self.molecule.coords[input_type]):
                input_file.write(f" {self.molecule.atoms[i].atomic_symbol}    {float(atom[0]): .10f}  {float(atom[1]): .10f}  {float(atom[2]): .10f} \n")

            input_file.write(f" units angstrom\n no_reorient\n}}\n\nset {{\n basis {self.molecule.basis}\n")
            input_file.write(setters)
            input_file.write(tasks)
        if execute:
            with open('log.txt', 'w+') as (log):
                try:
                    sp.run(f"psi4 input.dat -n {self.molecule.threads}", shell=True, stdout=log, stderr=log, check=True)
                except sp.CalledProcessError:
                    raise Psi4Error('Psi4 did not execute successfully check log file for details.')

            return self.check_for_errors()
        return {'success':False, 
         'error':'Not run'}

    def check_for_errors(self):
        """
        Read the output file from the job and check for normal termination and any errors
        :return: A dictionary of the success status and any problems.
        """
        with open('output.dat', 'r') as (log):
            for line in log:
                if '*** Psi4 exiting successfully.' in line:
                    return {'success': True}
                    if '*** Psi4 encountered an error.' in line:
                        return {'success':False, 
                         'error':'Not known'}

            return {'success':False, 
             'error':'Segfault'}

    def hessian(self):
        """
        Parses the Hessian from the output.dat file (from psi4) into a numpy array;
        performs check to ensure it is symmetric;
        has some basic error handling for if the file is missing data etc.
        """
        hess_size = 3 * len(self.molecule.atoms)
        with open('output.dat', 'r') as (file):
            lines = file.readlines()
            for count, line in enumerate(lines):
                if '## Hessian' in line or '## New Matrix (Symmetry' in line:
                    hess_start = count + 5
                    break
            else:
                raise EOFError('Cannot locate Hessian matrix in output.dat file.')

            extra = 0 if hess_size % 5 == 0 else 1
            hess_length = hess_size // 5 * hess_size + (hess_size // 5 - 1) * 3 + extra * (3 + hess_size)
            hess_end = hess_start + hess_length
            hess_vals = []
            for file_line in lines[hess_start:hess_end]:
                row_vals = [float(val) for val in file_line.split() if len(val) > 5]
                hess_vals.append(row_vals)

            hess_vals = [elem for elem in hess_vals if elem]
            reshaped = []
            for old_row in range(hess_size):
                new_row = []
                for col_block in range(hess_size // 5 + extra):
                    new_row += hess_vals[(old_row + col_block * hess_size)]

                reshaped.append(new_row)

            hess_matrix = np.array(reshaped)
            conversion = constants.HA_TO_KCAL_P_MOL / constants.BOHR_TO_ANGS ** 2
            hess_matrix *= conversion
            check_symmetry(hess_matrix)
            return hess_matrix

    def optimised_structure(self):
        """
        Parses the final optimised structure from the output.dat file (from psi4) to a numpy array.
        Also returns the energy of the optimized structure.
        """
        with open('output.dat', 'r') as (file):
            lines = file.readlines()
            geo_pos_list = []
            for count, line in enumerate(lines):
                if '==> Geometry' in line:
                    geo_pos_list.append(count)

            if not (opt_pos and opt_steps):
                raise EOFError('According to the output.dat file, optimisation has not completed.')
            opt_energy = float(lines[(opt_pos + opt_steps + 7)].split()[1])
            start_of_vals = geo_pos_list[(-1)] + 9
            opt_struct = []
            for row in range(len(self.molecule.atoms)):
                struct_row = []
                for indx in range(3):
                    struct_row.append(float(lines[(start_of_vals + row)].split()[(indx + 1)]))

                opt_struct.append(struct_row)

        return (
         np.array(opt_struct), opt_energy)

    @staticmethod
    def get_energy():
        """Get the energy of a single point calculation."""
        with open('output.dat', 'r') as (log):
            for line in log:
                if 'Total Energy =' in line:
                    return float(line.split()[3])

        raise EOFError('Cannot find energy in output.dat file.')

    def all_modes(self):
        """Extract all modes from the psi4 output file."""
        with open('output.dat', 'r') as (file):
            lines = file.readlines()
            for count, line in enumerate(lines):
                if 'post-proj  all modes' in line:
                    start_of_vals = count
                    break
            else:
                raise EOFError('Cannot locate modes in output.dat file.')

            end_of_vals = start_of_vals + 3 * len(self.molecule.atoms) // 6
            structures = lines[start_of_vals][24:].replace("'", '').split()
            structures = structures[6:]
            for row in range(1, end_of_vals - start_of_vals):
                structures += lines[(start_of_vals + row)].replace("'", '').replace(']', '').split()

            all_modes = [float(val) for val in structures]
            return np.array(all_modes)

    def geo_gradient(self, input_type='input', threads=False, execute=True):
        """
        Write the psi4 style input file to get the gradient for geometric
        and run geometric optimisation.
        """
        molecule = self.molecule.coords[input_type]
        with open(f"{self.molecule.name}.psi4in", 'w+') as (file):
            file.write(f"memory {self.molecule.memory} GB\n\nmolecule {self.molecule.name} {{\n {self.molecule.charge} {self.molecule.multiplicity} \n")
            for i, atom in enumerate(molecule):
                file.write(f"  {self.molecule.atoms[i].atomic_symbol:2}    {float(atom[0]): .10f}  {float(atom[1]): .10f}  {float(atom[2]): .10f}\n")

            file.write(f" units angstrom\n no_reorient\n}}\nset basis {self.molecule.basis}\n")
            if threads:
                file.write(f"set_num_threads({self.molecule.threads})")
            file.write(f"\n\ngradient('{self.molecule.theory}')\n")
        if execute:
            with open('log.txt', 'w+') as (log):
                sp.run(f"geometric-optimize --psi4 {self.molecule.name}.psi4in {self.molecule.constraints_file} --nt {self.molecule.threads}", shell=True,
                  stdout=log,
                  stderr=log)
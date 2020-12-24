# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/dihedrals.py
# Compiled at: 2019-09-30 09:58:49
# Size of source mod 2**32: 57471 bytes
from QUBEKit.engines import PSI4, OpenMM, Gaussian, RDKit
from QUBEKit.utils import constants
from QUBEKit.utils.decorators import timer_logger, for_all_methods
from QUBEKit.utils.exceptions import TorsionDriveFailed
from QUBEKit.utils.helpers import make_and_change_into
from collections import OrderedDict
from copy import deepcopy
import os
from shutil import rmtree
import subprocess as sp
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import minimize, differential_evolution
from scipy.stats import linregress
from datetime import datetime

@for_all_methods(timer_logger)
class TorsionScan:
    __doc__ = '\n    This class will take a QUBEKit molecule object and perform a torsiondrive QM energy scan\n    for each selected rotatable dihedral.\n\n    inputs\n    ---------------\n    molecule                A QUBEKit Ligand instance\n    constraints_made        The name of the constraints file that should be used during the torsiondrive (pis4 only)\n\n    attributes\n    ---------------\n    qm_engine               An instance of the QM engine used for any calculations\n    native_opt              Chosen dynamically whether to use geometric or not (geometric is need to use constraints)\n    inputfile               The name of the template file for tdrive, name depends on the qm_engine used\n    grid_space              The distance between the scan points on the surface\n    scan_start              The starting angle of the dihedral during the scan\n    scan_end                The final angle of the dihedral\n    home                    The starting location of the job, helpful when scanning multiple angles.\n    '

    def __init__(self, molecule, constraints_made=None):
        self.qm_engine = {'psi4':PSI4, 
         'g09':Gaussian,  'g16':Gaussian}.get(molecule.bonds_engine)(molecule)
        self.native_opt = True
        if molecule.geometric:
            if molecule.bonds_engine == 'psi4':
                self.native_opt = False
        self.input_file = None
        self.molecule = molecule
        self.molecule.convergence = 'GAU'
        self.constraints_made = constraints_made
        self.grid_space = molecule.increment
        self.scan_start = molecule.dih_start
        self.scan_end = molecule.dih_end
        self.home = os.getcwd()

    def find_scan_order(self):
        """
        Function takes the molecule and displays the rotatable central bonds,
        the user then enters the numbers of the torsions to be scanned (in the order they'll be scanned in).
        The molecule can also be supplied with a scan order already, if coming from csv.
        Else the user can supply a torsiondrive style QUBE_torsions.txt file we can extract the parameters from.
        """
        if self.molecule.scan_order:
            return self.molecule
        if self.molecule.rotatable is None:
            print('No rotatable torsions found in the molecule')
            self.molecule.scan_order = []
        else:
            if len(self.molecule.rotatable) == 1:
                print('One rotatable torsion found')
                self.molecule.scan_order = self.molecule.rotatable
            else:
                rotatable = list(self.molecule.rotatable)
                print('Please select the central bonds round which you wish to scan in the order to be scanned')
                print('Torsion number   Central-Bond   Representative Dihedral')
                for i, bond in enumerate(rotatable):
                    print(f"  {i + 1}                    {bond[0]}-{bond[1]}             {self.molecule.atoms[self.molecule.dihedrals[bond][0][0]].atom_name}-{self.molecule.atoms[self.molecule.dihedrals[bond][0][1]].atom_name}-{self.molecule.atoms[self.molecule.dihedrals[bond][0][2]].atom_name}-{self.molecule.atoms[self.molecule.dihedrals[bond][0][3]].atom_name}")

                scans = input('>').split()
                scan_order = []
                for scan in scans:
                    scan_order.append(rotatable[(int(scan) - 1)])

                self.molecule.scan_order = scan_order

    def tdrive_scan_input(self, scan):
        """Function takes the rotatable dihedrals requested and writes a scan input file for torsiondrive."""
        with open('dihedrals.txt', 'w+') as (out):
            out.write('# dihedral definition by atom indices starting from 0\n#zero_based_numbering\n# i     j     k     l     ')
            if self.molecule.dih_start != -165 or self.molecule.dih_end != 180:
                out.write('(range_low)     (range_high)\n')
            else:
                out.write('\n')
            scan_di = self.molecule.dihedrals[scan][0]
            out.write(f"  {scan_di[0]}     {scan_di[1]}     {scan_di[2]}     {scan_di[3]}     ")
            if self.molecule.dih_start != -165 or self.molecule.dih_end != 180:
                out.write(f"{self.molecule.dih_start}     {self.molecule.dih_end}\n")
            else:
                out.write('\n')
        if self.native_opt:
            self.qm_engine.generate_input(optimise=True, execute=False, red_mode=True)
            if self.qm_engine.__class__.__name__.lower() == 'psi4':
                self.input_file = 'input.dat'
            else:
                self.input_file = f"gj_{self.molecule.name}.com"
        else:
            self.qm_engine.geo_gradient(execute=False, threads=True)
            self.input_file = f"{self.molecule.name}.{self.qm_engine.__class__.__name__.lower()}in"

    def start_torsiondrive(self, scan):
        """Start a torsiondrive either using psi4 or native gaussian09"""
        self.tdrive_scan_input(scan)
        with open('tdrive.log', 'w') as (log):
            log.write(f"Theory used: {self.molecule.theory}   Basis used: {self.molecule.basis}\n")
            log.flush()
            tdrive_engine = self.qm_engine.__class__.__name__.lower()
            cmd = f"torsiondrive-launch -e {tdrive_engine} {self.input_file} dihedrals.txt -v {'--native_opt' if self.native_opt else ''}"
            sp.run(cmd, shell=True, stdout=log, check=True, stderr=log, bufsize=0)
        try:
            self.molecule.read_tdrive(scan)
        except FileNotFoundError:
            raise TorsionDriveFailed('Torsiondrive output qdata.txt missing; job did not execute or finish properly')

    def collect_scan(self):
        """
        Collect the results of a torsiondrive scan that has not been done using QUBEKit.
        :return: The energies and coordinates into the molecule
        """
        for scan in self.molecule.scan_order:
            os.chdir(os.path.join(self.home, os.path.join(f"SCAN_{scan[0]}_{scan[1]}", 'QM_torsiondrive')))
            self.molecule.read_tdrive(scan)

    def check_run_history(self, scan):
        """
        Check the contents of a scan folder to see if we should continue the run;
        if the settings (theory and basis) are the same then continue
        :return: If we should continue the run
        """
        try:
            file_path = os.path.join(os.getcwd(), os.path.join(f"SCAN_{scan[0]}_{scan[1]}", os.path.join('QM_torsiondrive', 'tdrive.log')))
            with open(file_path) as (t_log):
                header = t_log.readline().split('Basis used:')
            basis = header[1].strip()
            theory = header[0].split('Theory used:')[1].strip()
            return self.molecule.theory == theory and self.molecule.basis == basis
        except FileNotFoundError:
            return False

    def scan(self):
        """Makes a folder and writes a new a dihedral input file for each scan and runs the scan."""
        for scan in self.molecule.scan_order:
            try:
                os.mkdir(f"SCAN_{scan[0]}_{scan[1]}")
            except FileExistsError:
                con_scan = self.check_run_history(scan)
                if not con_scan:
                    print(f"SCAN_{scan[0]}_{scan[1]} folder present backing up folder to SCAN_{scan[0]}_{scan[1]}_tmp")
                    try:
                        rmtree(f"SCAN_{scan[0]}_{scan[1]}_tmp")
                    except FileNotFoundError:
                        pass

                    os.system(f"mv SCAN_{scan[0]}_{scan[1]} SCAN_{scan[0]}_{scan[1]}_tmp")
                    os.mkdir(f"SCAN_{scan[0]}_{scan[1]}")

            os.chdir(f"SCAN_{scan[0]}_{scan[1]}")
            make_and_change_into('QM_torsiondrive')
            self.start_torsiondrive(scan)
            os.chdir(self.home)


@for_all_methods(timer_logger)
class TorsionOptimiser:
    __doc__ = '\n    Torsion optimiser class used to optimise dihedral parameters with a range of methods\n\n    inputs\n    ---------\n    # Configurations\n    l_pen\n    t_weight\n    weight_mm:              Weight the low energy parts of the surface (not sure if it works)\n    step_size:              The scipy displacement step size\n    methods\n    method\n    error_tol\n    x_tol:\n    use_force:              Match the forces as well as the energies (not available yet)\n    abs_bounds\n    refinement:             The stage two refinement methods\n\n    # QUBEKit Internals\n    molecule\n    qm_engine\n\n    # TorsionOptimiser starting parameters\n    scans_dict             QM scan energies {(scan): [array of qm energies]}\n    mm_energy               numpy array of the current mm energies\n    initial_energy          numpy array of the fitting iteration initial parameter energies\n    starting_energy         numpy array of the starting parameter energies\n    scan_order              list of the scan keys in the order to be fit\n    scan_coords             list of molecule geometries in OpenMM format list[tuple] [(x, y, z)]\n    starting_params         list of the dihedral starting parameters\n    energy_store_qm         list of all of the qm energies collected in the same order as the scan coords\n    coords_store            list of all of the coordinates sampled in the fitting\n    initial_coords          the qm optimised geometries\n    tor_types               important! stores the torsion indices in the OpenMM system and groups torsions\n    target_energy           list of the qm optimised energies\n    qm_energy               the current qm energy numpy array\n    scan                    the current scan key that is being fit\n    param_vector            numpy array of the parameters being fit, this is a flat array even with multiple torsions\n    torsion_store           this dictionary is a copy of the molecules periodic torsion force dict\n    index_dict              used to work out the index of the torsions in the OpenMM system\n    qm_local                the location of the QM torsiondrive\n    '

    def __init__(self, molecule, weight_mm=True, step_size=0.02, error_tol=1e-05, x_tol=1e-05):
        self.molecule = molecule
        self.qm_engine = {'psi4':PSI4,  'g09':Gaussian,  'g16':Gaussian}.get(self.molecule.bonds_engine)(molecule)
        self.weight_mm = weight_mm
        self.step_size = step_size
        self.error_tol = error_tol
        self.x_tol = x_tol
        self.l_pen = self.molecule.l_pen
        self.t_weight = self.molecule.t_weight
        self.abs_bounds = molecule.tor_limit
        self.refinement = molecule.refinement_method
        self.methods = {'NM':'Nelder-Mead', 
         'BFGS':'BFGS',  'GA':'Genetic'}
        self.method = self.methods.get(self.molecule.opt_method, None)
        self.scans_dict = deepcopy(molecule.qm_scans)
        self.mm_energy = None
        self.initial_energy = None
        self.starting_energy = None
        self.scan_order = molecule.scan_order
        self.scan_coords = None
        self.starting_params = []
        self.energy_store_qm = []
        self.coords_store = []
        self.initial_coords = []
        self.tor_types = OrderedDict()
        self.target_energy = None
        self.qm_energy = None
        self.scan = None
        self.param_vector = None
        self.torsion_store = None
        self.index_dict = {}
        self.qm_local = None
        self.rmsd_atoms = []
        self.optimiser_log = None
        self.opt_coords = self.molecule.openmm_coordinates(input_type='qm')
        self.k_b = constants.KB_KCAL_P_MOL_K
        self.phases = [0, constants.PI, 0, constants.PI]
        self.home = os.getcwd()
        self.molecule.write_pdb()
        self.load_torsions()
        self.open_mm = OpenMM(self.molecule)

    def mm_energies(self):
        """
        Evaluate the MM energies of the geometries stored in scan_coords.
        :return: A numpy array of the energies for easy normalisation.
        """
        return np.array([self.open_mm.get_energy(position) for position in self.scan_coords])

    def reset_torsions(self):
        """Reset all torsion values to their initial and create the torsion index dictionary."""
        forces = {self.open_mm.simulation.system.getForce(index).__class__.__name__:self.open_mm.simulation.system.getForce(index) for index in range(self.open_mm.simulation.system.getNumForces())}
        torsion_force = forces['PeriodicTorsionForce']
        for i in range(torsion_force.getNumTorsions()):
            *torsion, _, _, _ = torsion_force.getTorsionParameters(i)
            torsion = tuple(torsion)
            if torsion not in self.index_dict:
                self.index_dict[torsion] = i

        improper_index_keys = [tuple(sorted(key)) for key in self.index_dict.keys()]
        for pos, key in enumerate(self.torsion_store):
            try:
                self.tor_types[pos] = [
                 [
                  key], [float(self.torsion_store[key][i][1]) for i in range(4)],
                 [
                  self.index_dict[key]]]
            except KeyError:
                try:
                    self.tor_types[pos] = [
                     [
                      tuple(reversed(key))], [float(self.torsion_store[key][i][1]) for i in range(4)],
                     [
                      self.index_dict[tuple(reversed(key))]]]
                except KeyError:
                    improper_key = list(self.index_dict.keys())[improper_index_keys.index(tuple(sorted(key)))]
                    self.tor_types[pos] = [[improper_key], [float(self.torsion_store[key][i][1]) for i in range(4)],
                     [
                      self.index_dict[improper_key]]]

        self.update_torsions()
        self.tor_types = OrderedDict()

    def update_tor_vec(self, x):
        """Update the tor_types dict with the parameter vector."""
        x = np.round(x, decimals=6)
        for key, val in self.tor_types.items():
            val[1] = x[key * 4:key * 4 + 4]

    def objective(self, x):
        """Return the output of the objective function."""
        self.update_tor_vec(x)
        self.update_torsions()
        self.mm_energy = deepcopy(self.mm_energies())
        if not len(self.qm_energy) == len(self.mm_energy):
            raise AssertionError
        elif self.molecule.relative_to_global:
            mm_energy = self.mm_energy - self.open_mm.get_energy(self.opt_coords)
        else:
            mm_energy = self.mm_energy - self.mm_energy.min()
        error = (mm_energy - self.qm_energy) ** 2
        if self.t_weight != 'infinity':
            error *= np.exp(-self.qm_energy / (self.k_b * self.t_weight))
        total_error = np.sqrt(sum(error) / len(self.scan_coords))
        move_pen = self.l_pen * sum((x - self.starting_params) ** 2)
        bounds_pen = sum((1 for vn in x if abs(vn) >= self.abs_bounds))
        total_error += move_pen + bounds_pen
        return total_error

    def steep_objective(self, x):
        """Return the output of the objective function when using the steep refinement method."""
        self.update_tor_vec(x)
        self.update_torsions()
        self.scan_coords = self.drive_mm('geometric')
        self.mm_energy = self.mm_energies()
        assert len(self.qm_energy) == len(self.mm_energy)
        self.mm_energy -= self.mm_energy.min()
        error = (self.mm_energy - self.qm_energy) ** 2
        if self.t_weight != 'infinity':
            error *= np.exp(-self.qm_energy / (self.k_b * self.t_weight))
        total_error = np.sqrt(sum(error) / len(self.scan_coords))
        pen = self.l_pen * sum((x - self.starting_params) ** 2)
        total_error += pen
        return total_error

    def single_point_matching(self, fitting_error, opt_parameters):
        """A function the call the single point matching method of parameter refinement.

        method (fit only new generation)
        -------------------
        1) take parameters from the initial scipy fitting.
        2) Do a MM torsion scan with the parameters and get the rmsd error and energy error between this new surface
        and the qm optimised surface
        3) Now fit to the qm surface again using a small restrain penalty
        """
        converged = False
        self.method = self.methods.get(self.molecule.opt_method.split('_')[(-1)], None)
        print(f"The optimisation method is {self.method}")
        objective = {'fitting_error':[],  'energy_error':[],  'rmsd':[],  'total':[],  'parameters':[]}
        iteration = 1
        while not converged:
            make_and_change_into(f"Iteration_{iteration}")
            self.scan_coords = self.drive_mm('torsiondrive')
            self.coords_store = deepcopy(self.coords_store + self.scan_coords)
            rmsd_vector = self.scan_rmsd(self.scan_coords)
            energy_error = self.objective(opt_parameters)
            self.initial_energy = deepcopy(self.mm_energy)
            objective['fitting_error'].append(fitting_error)
            objective['energy_error'].append(energy_error)
            objective['rmsd'].append(sum(rmsd_vector) / len(rmsd_vector))
            objective['total'].append(energy_error + sum(rmsd_vector) / len(rmsd_vector))
            objective['parameters'].append(opt_parameters)
            if objective['total'][(-1)] <= 0.25:
                converged = True
                print(f"Fitting converged after {iteration} iterations exiting...")
                iteration = 5
            self.optimiser_log.write('After refinement the errors are:\n')
            for error, value in objective.items():
                self.optimiser_log.write(f"{error}: {value}\n")

            self.optimiser_log.flush()
            if iteration < 5:
                self.starting_params = opt_parameters
                self.l_pen = 0.15
                fitting_error, opt_parameters = self.scipy_optimiser()
                self.update_tor_vec(opt_parameters)
                self.update_mol()
                self.mm_energy = deepcopy(self.mm_energies())
                self.optimiser_log.write(f"Results for fitting iteration: {iteration}\n")
                self.optimiser_log.flush()
                self.plot_results(name=f"SP_iter_{iteration}")
                os.chdir('../')
                iteration += 1
            else:
                self.mm_energy = deepcopy(self.mm_energies())
                self.plot_results(name=f"SP_iter_{iteration}")
                os.chdir('../')
                break

        min_error = min(objective['total'])
        min_index = objective['total'].index(min_error)
        final_parameters = deepcopy(objective['parameters'][min_index])
        final_error = objective['total'][min_index]
        self.optimiser_log.write(f"The lowest error:{final_error}\nThe corresponding parameters:{final_parameters}\nwere found on iteraion {min_index + 1}")
        self.optimiser_log.flush()
        self.scan_coords = self.initial_coords
        final_surface_energy = deepcopy(self.mm_energy)
        energy_error = self.objective(final_parameters)
        self.optimiser_log.write(f"The final error at the qm optimised geometries is {energy_error}\n")
        self.initial_energy = self.starting_energy
        self.optimiser_log.write('The final stage 2 fitting results:\n')
        self.optimiser_log.flush()
        self.plot_results(name='Stage2_Single_point_fit', extra_points={'Final parameters MM geometry': final_surface_energy})
        self.plot_convergence(objective)
        self.plot_correlation(final_parameters)
        return (
         final_error, final_parameters)

    def qm_normalise(self):
        """
        Normalize the qm energy to the reference energy which is either the lowest in the set or the global minimum
        :return: normalised qm vector
        """
        if self.molecule.relative_to_global:
            self.qm_energy -= self.molecule.qm_energy
            print('Using the optimised structure!')
        else:
            self.qm_energy -= self.qm_energy.min()
        self.qm_energy *= constants.HA_TO_KCAL_P_MOL

    def torsion_test(self):
        """
        Take optimized xml file and test the agreement with QM by doing a torsion drive and checking the single
        point energies for each rotatable dihedral.
        """
        for i, self.scan in enumerate(self.molecule.scan_order):
            make_and_change_into(f"SCAN_{self.scan[0]}_{self.scan[1]}")
            try:
                rmtree('testing_torsion')
            except FileNotFoundError:
                pass

            make_and_change_into('testing_torsion')
            self.scan_coords = self.drive_mm('torsiondrive')
            self.qm_energy = self.single_point()
            self.qm_normalise()
            self.reset_torsions()
            self.mm_energy = deepcopy(self.starting_energy)
            self.plot_results(name='testing_torsion', torsion_test=True)
            os.chdir('../../')

    def run(self):
        """
        Optimise the parameters for the chosen torsions in the molecule scan_order,
        also set up a work queue to do the single point calculations if they are needed.
        """
        for self.scan in self.scan_order:
            self.molecule.coords['traj'] = self.molecule.qm_scans[self.scan][1]
            self.scan_coords = self.molecule.openmm_coordinates(input_type='traj')
            if not self.rmsd_atoms:
                self._create_rdkit_molecules(self.scan_coords)
            try:
                os.mkdir(f"SCAN_{self.scan[0]}_{self.scan[1]}")
            except FileExistsError:
                os.rename(f"SCAN_{self.scan[0]}_{self.scan[1]}", f"SCAN_{self.scan[0]}_{self.scan[1]}_backup")
                os.mkdir(f"SCAN_{self.scan[0]}_{self.scan[1]}")

            os.chdir(f"SCAN_{self.scan[0]}_{self.scan[1]}")
            self.optimiser_log = open('Optimiser_log.txt', 'w')
            self.optimiser_log.write(f"Starting dihedral optimisation at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n")
            self.optimiser_log.write(f"Optimising dihedrals for central bond {self.scan}\n")
            self.optimiser_log.flush()
            os.mkdir('First_fit')
            os.mkdir('Refinement')
            os.chdir('First_fit')
            self.target_energy = self.scans_dict[self.scan][0]
            self.energy_store_qm = deepcopy(self.target_energy)
            self.qm_energy = deepcopy(self.target_energy)
            self.qm_normalise()
            self.coords_store = deepcopy(self.scan_coords)
            self.initial_coords = deepcopy(self.scan_coords)
            self.reset_torsions()
            self.get_torsion_params()
            starting_error = deepcopy(self.objective(self.starting_params))
            self.initial_energy = deepcopy(self.mm_energy)
            self.starting_energy = deepcopy(self.initial_energy)
            self.optimiser_log.write(f"Starting initial optimisation\nThe starting error is: {starting_error}\n")
            self.optimiser_log.flush()
            self.method = self.methods.get(self.molecule.opt_method.split('_')[0], None)
            error, opt_parameters = self.scipy_optimiser()
            self.optimiser_log.write(f"fitted parameters {opt_parameters}\n")
            self.optimiser_log.write(f"Fitted error {error}\n")
            self.optimiser_log.flush()
            self.param_vector = opt_parameters
            self.update_mol()
            self.optimiser_log.write('Optimisation finished\n')
            self.optimiser_log.flush()
            self.plot_results(name='Stage1_scipy')
            os.chdir('../Refinement')
            if self.refinement == 'SP':
                self.optimiser_log.write('Starting refinement method single point matching\n')
                self.optimiser_log.flush()
                error, opt_parameters = self.single_point_matching(error, opt_parameters)
                self.param_vector = opt_parameters
            else:
                if self.refinement == 'Steep':
                    error, opt_parameters = self.steepest_decent_refinement(self.param_vector)
                self.update_tor_vec(opt_parameters)
                self.update_mol()
                os.chdir(self.home)
                self.optimiser_log.write(f"Optimisation finished at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n")
                self.optimiser_log.flush()
                self.optimiser_log.close()

    def steepest_decent_refinement(self, x):
        """
        A steepest descent optimiser as implemented in QUBEKit-V1, which will optimise the torsion terms
        using full relaxed surface scans. SLOW!
        """
        print('Starting optimisation ...')
        step_size = [
         0.1, 0.01, 0.001]
        step_index = 0
        converged = False
        final_error = None
        final_parameters = None
        while not converged:
            un_changed = 0
            for i in range(len(x)):
                error = {}
                self.scan_coords = self.drive_mm('geometric')
                normal = self.objective(x)
                error[normal] = x
                y_plus = deepcopy(x)
                y_plus[i] += step_size[step_index]
                print(f"y plus {y_plus}")
                self.scan_coords = self.drive_mm('geometric')
                error_plus = self.objective(y_plus)
                error[error_plus] = y_plus
                y_minus = deepcopy(x)
                y_minus[i] -= step_size[step_index]
                print(f"y minus {y_minus}")
                self.scan_coords = self.drive_mm('geometric')
                error_minus = self.objective(y_minus)
                error[error_minus] = y_minus
                min_error = min(normal, error_plus, error_minus)
                print(f"minimum error {min_error}")
                x = deepcopy(error[min_error])
                print(f"The new parameter vector {x}")
                if min_error == normal:
                    un_changed += 1
                if un_changed == len(x) - 1:
                    step_index += 1
                if step_index >= len(step_size):
                    final_parameters = deepcopy(x)
                    final_error = deepcopy(min_error)
                    converged = True

        return (
         final_error, final_parameters)

    def load_torsions(self):
        """
        Set all the torsion k values to one for every torsion in the system.

        Once an OpenMM system is created we cannot add new torsions without making a new PeriodicTorsion
        force every time.

        To get round this we have to load every k parameter into the system first; so we set every k term in the fitting
        dihedrals to 1 then reset all values to the gaff terms and update in context.
        """
        self.torsion_store = deepcopy(self.molecule.PeriodicTorsionForce)
        for key in self.molecule.PeriodicTorsionForce:
            if self.molecule.PeriodicTorsionForce[key][(-1)] == 'Improper':
                self.molecule.PeriodicTorsionForce[key] = [
                 [
                  '1', '1', '0'], ['2', '1', (f"{constants.PI}")],
                 [
                  '3', '1', '0'], ['4', '1', (f"{constants.PI}")], 'Improper']
            else:
                self.molecule.PeriodicTorsionForce[key] = [
                 [
                  '1', '1', '0'], ['2', '1', (f"{constants.PI}")],
                 [
                  '3', '1', '0'], ['4', '1', (f"{constants.PI}")]]

        self.molecule.write_parameters()
        self.molecule.PeriodicTorsionForce = deepcopy(self.torsion_store)

    def get_torsion_params(self):
        """
        Get the torsions and their parameters that will scanned, work out how many different torsion types needed,
        make a vector corresponding to this size.
        """
        to_fit = [tuple(tor) for tor in list(self.molecule.dihedrals[self.scan])]
        torsions_and_types = {}
        for key, dihedral_class in self.molecule.dihedral_types.items():
            for dihedral in dihedral_class:
                if dihedral in to_fit or tuple(reversed(dihedral)) in to_fit:
                    torsions_and_types[key] = dihedral_class
                    break

        self.tor_types = OrderedDict()
        i = 0
        for symmetry_key, torsions in torsions_and_types.items():
            torsion = torsions[0]
            try:
                master_vector = [float(self.torsion_store[torsion][i][1]) for i in range(4)]
            except KeyError:
                torsion = torsion[::-1]
                master_vector = [float(self.torsion_store[torsion][i][1]) for i in range(4)]

            self.tor_types[i] = [torsions, master_vector, [], symmetry_key]
            for torsion in torsions:
                try:
                    self.tor_types[i][2].append(self.index_dict[torsion])
                except KeyError:
                    self.tor_types[i][2].append(self.index_dict[tuple(reversed(torsion))])

            i += 1

        self.param_vector = np.array([0 for _ in range(4) for _ in range(len(self.tor_types))])
        self.starting_params = np.array([list(k)[1][i] for k in self.tor_types.values() for i in range(4)])
        self.optimiser_log.write(f"Starting parameters {self.starting_params}\n")
        self.optimiser_log.flush()

    def _create_rdkit_molecules(self, coordinates):
        """
        Create a list of rdkit molecules corresponding to the coordinates of the qm torsionscan, these are used to compute
        the rmsd.
        :param coordinates: A list of numpy arrays used to generate the conformers
        :return: a list of rdkit molecules each corresponding to a point on the torsionscan
        """
        for coord in coordinates:
            rdkit_mol = deepcopy(self.molecule.rdkit_mol)
            rdkit_mol.RemoveAllConformers()
            rdkit_mol = RDKit().add_conformer(rdkit_mol, np.array(coord) * constants.NM_TO_ANGS)
            self.rmsd_atoms.append(rdkit_mol)

    def scan_rmsd(self, coordinates):
        """
        Calculate the rmsd between the stored qm positions and the new set of coordinates
        :param coordinates:  A list of numpy coordinate arrays
        :return: a list containing the rmsd values for each pair of coordinates
        """
        assert len(coordinates) == len(self.rmsd_atoms)
        rmsd = []
        for coord, molecule in zip(coordinates, self.rmsd_atoms):
            molecule = RDKit().add_conformer(molecule, np.array(coord) * constants.NM_TO_ANGS)
            rmsd.append(RDKit().get_conformer_rmsd(molecule, 0, molecule.GetNumConformers() - 1))

        return rmsd

    def finite_difference(self, x):
        """Compute the gradient of changing the parameter vector using central difference scheme."""
        gradient = []
        for i in range(len(x)):
            x[i] += self.step_size / 2
            plus = self.objective(x)
            x[i] -= self.step_size
            minus = self.objective(x)
            diff = (plus - minus) / self.step_size
            gradient.append(diff)

        return np.array(gradient)

    def scipy_optimiser(self):
        """The main torsion parameter optimiser that controls the optimisation method used."""
        print(f"Running SciPy {self.method} optimiser ... ")
        if self.method == 'Nelder-Mead':
            res = minimize((self.objective), (self.param_vector), method=(self.method), options={'xtol':self.x_tol, 
             'ftol':self.error_tol,  'disp':True,  'maxiter':10000})
        else:
            if self.method == 'BFGS':
                res = minimize((self.objective), (self.param_vector), method=(self.method), jac=(self.finite_difference), options={'disp': True})
            else:
                if self.method == 'Genetic':
                    print(self.param_vector)
                    bounds = [(-abs(self.abs_bounds), abs(self.abs_bounds)) for _ in range(len(self.param_vector))]
                    print(bounds)
                    res = differential_evolution((self.objective), bounds=bounds)
                else:
                    raise NotImplementedError('This optimisation method is not implemented; options are: Nelder-Mead, BFGS, Genetic.')
        print('SciPy optimisation complete')
        self.update_tor_vec(res.x)
        return (
         res.fun, res.x)

    def update_torsions(self):
        """Update the torsions being fitted."""
        forces = {self.open_mm.simulation.system.getForce(index).__class__.__name__:self.open_mm.simulation.system.getForce(index) for index in range(self.open_mm.simulation.system.getNumForces())}
        torsion_force = forces['PeriodicTorsionForce']
        for val in self.tor_types.values():
            for j, dihedral in enumerate(val[0]):
                for v_n in range(4):
                    torsion_force.setTorsionParameters(index=(v_n + val[2][j]),
                      periodicity=(v_n + 1),
                      phase=(self.phases[v_n]),
                      k=(val[1][v_n]),
                      particle1=(dihedral[0]),
                      particle2=(dihedral[1]),
                      particle3=(dihedral[2]),
                      particle4=(dihedral[3]))

        torsion_force.updateParametersInContext(self.open_mm.simulation.context)
        return self.open_mm

    def plot_results(self, name='Plot', torsion_test=False, extra_points=None):
        """
        Plot the results of the scan.
        :param name: Name of the pdf made
        :param torsion_test: changes the style of the plot for testing
        :param extra_points: a dictionary of label's and extra points to plot
        :return:
        """
        assert len(self.qm_energy) == len(self.mm_energy)
        if self.molecule.relative_to_global:
            if torsion_test:
                initial_energy = self.mm_energy - self.open_mm.get_energy(self.opt_coords)
                plot_mm_energy = initial_energy
            else:
                plot_mm_energy = self.mm_energy - self.open_mm.get_energy(self.opt_coords)
                initial_energy = self.initial_energy - self.open_mm.get_energy(self.opt_coords)
            if extra_points is not None:
                for key, val in extra_points.items():
                    extra_points[key] = val - self.open_mm.get_energy(self.opt_coords)

        else:
            if torsion_test:
                initial_energy = self.mm_energy - self.mm_energy.min()
                plot_mm_energy = initial_energy
            else:
                plot_mm_energy = self.mm_energy - self.mm_energy.min()
                initial_energy = self.initial_energy - self.initial_energy.min()
            if extra_points is not None:
                for key, val in extra_points.items():
                    extra_points[key] = val - val.min()

        angles = list(range(self.molecule.dih_start, self.molecule.dih_end + self.molecule.increment, self.molecule.increment))
        assert len(angles) == len(self.qm_energy)
        if torsion_test:
            self.optimiser_log.write('Angle    QM(relative)        MM_initial(relative)\n')
            self.optimiser_log.flush()
            for data in zip(angles, self.qm_energy, initial_energy):
                self.optimiser_log.write(f"{data[0]:4}  {data[1]:15.10f}     {data[2]:15.10f}\n")
                self.optimiser_log.flush()

        else:
            self.optimiser_log.write('Angle    QM(relative)        MM(relative)    MM_initial(relative)\n')
            self.optimiser_log.flush()
            for data in zip(angles, self.qm_energy, plot_mm_energy, initial_energy):
                self.optimiser_log.write(f"{data[0]:4}  {data[1]:15.10f}     {data[2]:15.10f}    {data[3]:15.10f}\n")
                self.optimiser_log.flush()

        plt.xlabel('Dihedral angle$^{\\circ}$')
        plt.plot(angles, (self.qm_energy), 'o', label='QM data')
        if torsion_test:
            plt.plot(angles, initial_energy, label='Current parameters')
        else:
            plt.plot(angles, initial_energy, label='Starting parameters', linestyle='--')
            plt.plot(angles, plot_mm_energy, label='Final parameters')
            if extra_points is not None:
                for title, values in extra_points.items():
                    plt.plot(angles, values, label=title)

            mol_di = self.molecule.dihedrals[self.scan][0]
            plt.title(f"Relative energy surface for dihedral {mol_di[0]}-{mol_di[1]}-{mol_di[2]}-{mol_di[3]}")
            plt.ylabel('Relative energy (kcal/mol)')
            plt.legend(loc=1)
            plt.savefig(f"{name}.pdf")
            plt.clf()

    def plot_correlation(self, optimised_parameters):
        """Plot the single point energy correlation between all points in the fitting"""
        self.scan_coords = deepcopy(self.coords_store[:24])
        self.objective(optimised_parameters)
        mm_energy_new = self.mm_energy - self.mm_energy.min()
        slope_new, intercept_new, r_value_new, _, _ = linregress(self.qm_energy, mm_energy_new)
        self.objective(self.starting_params)
        mm_energy_old = self.mm_energy - self.mm_energy.min()
        slope_old, intercept_old, r_value_old, _, _ = linregress(self.qm_energy, mm_energy_old)
        assert len(self.qm_energy) == len(mm_energy_new)
        assert len(self.qm_energy) == len(mm_energy_old)
        plt.scatter((self.qm_energy), mm_energy_old, label=f"starting parameters $r^2$={r_value_old ** 2:.4f}", s=10)
        plt.scatter((self.qm_energy), mm_energy_new, label=f"Final parameters $r^2$={r_value_new ** 2:.4f}", s=10)
        x = np.linspace(self.qm_energy.min(), self.qm_energy.max(), 100)
        mm_min = min(mm_energy_new.min(), mm_energy_old.min())
        mm_max = max(mm_energy_new.max(), mm_energy_old.max())
        y = np.linspace(mm_min, mm_max, 100)
        plt.plot(x, y, ls='--', c='.3', zorder=2)
        plt.xlabel('Relative energy (kcal/mol) QM energy')
        plt.ylabel('Relative energy (kcal/mol) MM energy')
        plt.legend(loc=1)
        plt.savefig('correlation_plot.pdf')
        plt.clf()

    def plot_convergence(self, objective):
        """
        Plot the convergence of the errors through the iterative fitting methods
        :param objective: A dictionary containing all of the error measurements
        :return: None
        """
        iterations = [x for x in range(len(objective['total']))]
        fig, ax1 = plt.subplots()
        color = 'tab:red'
        ax1.set_xlabel('Fitting iteration')
        ax1.set_ylabel('Error (kcal / mol)', color=color)
        ax1.plot(iterations, (objective['energy_error']), label='Energy error', color=color, linestyle='--')
        ax1.plot(iterations, (objective['total']), label='Total error', color=color)
        ax1.tick_params(axis='y', labelcolor=color)
        color = 'tab:blue'
        ax2 = ax1.twinx()
        ax2.plot(iterations, (objective['rmsd']), label='RMSD error', color=color)
        ax2.set_ylabel('RMSD', color=color)
        ax2.tick_params(axis='y', labelcolor=color)
        lines, labels = ax1.get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend((lines + lines2), (labels + labels2), loc=1)
        fig.tight_layout()
        plt.savefig('convergence.pdf')
        plt.clf()

    def make_constraints(self):
        """Write a constraint file used by geometric during optimizations."""
        with open('qube_constraints.txt', 'w+') as (constraint):
            mol_di = self.molecule.dihedrals[self.scan][0]
            constraint.write(f"$scan\ndihedral {mol_di[0]} {mol_di[1]} {mol_di[2]} {mol_di[3]} -165.0 180 24\n")
            if self.molecule.constraints_file:
                with open(self.molecule.constraints_file) as (cons_file):
                    for line in cons_file:
                        constraint.write(line)

    def write_dihedrals(self):
        """Write out the torsion drive dihedral file for the current self.scan."""
        with open('dihedrals.txt', 'w+') as (out):
            out.write('# dihedral definition by atom indices starting from 0\n#zero_based_numbering\n# i     j     k     l\n')
            mol_di = self.molecule.dihedrals[self.scan][0]
            out.write(f"  {mol_di[0]}     {mol_di[1]}     {mol_di[2]}     {mol_di[3]}\n")

    def drive_mm(self, engine):
        """Drive the torsion again using MM to get new structures."""
        temp = f"{engine}_scan"
        try:
            rmtree(temp)
        except FileNotFoundError:
            pass

        make_and_change_into(temp)
        self.molecule.write_pdb(name='openmm')
        self.molecule.write_parameters(name='openmm')
        with open('log.txt', 'a+') as (log):
            if engine == 'torsiondrive':
                if self.molecule.constraints_file is not None:
                    os.system('mv ../constraints.txt .')
                self.write_dihedrals()
                sp.run(f"torsiondrive-launch -e openmm openmm.pdb dihedrals.txt -v {self.molecule.constraints_file if self.molecule.constraints_file is not None else ''}", shell=True,
                  stderr=log,
                  stdout=log,
                  check=True)
                self.molecule.read_tdrive(self.scan)
                self.molecule.coords['traj'] = self.molecule.qm_scans[self.scan][1]
                positions = self.molecule.openmm_coordinates(input_type='traj')
            else:
                if engine == 'geometric':
                    if self.molecule.constraints_file is not None:
                        os.system('mv ../constraints.txt .')
                    else:
                        self.make_constraints()
                    sp.run('geometric-optimize --reset --epsilon 0.0 --maxiter 500 --qccnv --pdb openmm.pdb --openmm state.xml qube_constraints.txt', shell=True,
                      stdout=log,
                      stderr=log,
                      check=True)
                    positions = self.molecule.read_xyz('scan.xyz')
                else:
                    raise NotImplementedError('Invalid torsion engine. Please use torsiondrive or geometric')
        os.chdir('../')
        return positions

    def single_point(self):
        """Take set of coordinates of a molecule and do a single point calculation; returns an array of the energies."""
        self.molecule.coords['temp'] = self.molecule.coords['input']
        try:
            rmtree('Single_points')
        except FileNotFoundError:
            pass

        make_and_change_into('Single_points')
        sp_energy = []
        for i, x in enumerate(self.scan_coords):
            make_and_change_into(f"SP_{i}")
            print(f"Doing single point calculations on new structures ... {i + 1}/{len(self.scan_coords)}")
            for y, coord in enumerate(x):
                for z, pos in enumerate(coord):
                    self.qm_engine.molecule.coords['temp'][y][z] = pos * 10

            result = self.qm_engine.generate_input(input_type='temp', energy=True)
            if result['success'] and self.qm_engine.__class__.__name__ == 'Gaussian':
                coords, energy = self.qm_engine.optimised_structure()
                sp_energy.append(energy)
            else:
                if result['success']:
                    if self.qm_engine.__class__.__name__ == 'PSI4':
                        sp_energy.append(PSI4.get_energy())
                os.chdir('../')

        os.chdir('../')
        return np.array(sp_energy)

    def update_mol(self):
        """When the optimisation is complete, update the PeriodicTorsionForce parameters in the molecule."""
        for val in self.tor_types.values():
            for dihedral in val[0]:
                for vn in range(4):
                    try:
                        self.molecule.PeriodicTorsionForce[dihedral][vn][1] = str(val[1][vn])
                    except KeyError:
                        self.molecule.PeriodicTorsionForce[tuple(reversed(dihedral))][vn][1] = str(val[1][vn])
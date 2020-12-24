# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/engines/openmm.py
# Compiled at: 2019-08-06 09:00:40
# Size of source mod 2**32: 9699 bytes
from QUBEKit.utils import constants
from QUBEKit.utils.decorators import timer_logger
import numpy as np
from simtk.openmm import app
import simtk.openmm as mm
from simtk import unit
import xml.etree.ElementTree as ET
from copy import deepcopy

class OpenMM:
    __doc__ = 'This class acts as a wrapper around OpenMM so we can many basic functions using the class'

    def __init__(self, molecule):
        self.molecule = molecule
        self.system = None
        self.simulation = None
        self.combination = molecule.combination
        self.pdb = molecule.name + '.pdb'
        self.xml = molecule.name + '.xml'
        self.openmm_system()

    @timer_logger
    def openmm_system(self):
        """Initialise the OpenMM system we will use to evaluate the energies."""
        pdb = app.PDBFile(self.pdb)
        forcefield = app.ForceField(self.xml)
        modeller = app.Modeller(pdb.topology, pdb.positions)
        self.system = forcefield.createSystem((modeller.topology), nonbondedMethod=(app.NoCutoff), constraints=None)
        xmlstr = open(self.xml).read()
        try:
            self.combination = ET.fromstring(xmlstr).find('NonbondedForce').attrib['combination']
        except AttributeError:
            pass
        except KeyError:
            pass

        if self.combination == 'opls':
            print('OPLS combination rules found in xml file')
            self.opls_lj()
        temperature = constants.STP * unit.kelvin
        integrator = mm.LangevinIntegrator(temperature, 5 / unit.picoseconds, 0.001 * unit.picoseconds)
        self.simulation = app.Simulation(modeller.topology, self.system, integrator)
        self.simulation.context.setPositions(modeller.positions)

    def get_energy(self, position):
        """
        Return the MM calculated energy of the structure
        :param position: The OpenMM formatted atomic positions
        :return:
        """
        self.simulation.context.setPositions(position)
        state = self.simulation.context.getState(getEnergy=True)
        energy = state.getPotentialEnergy().value_in_unit(unit.kilocalories_per_mole)
        return energy

    @timer_logger
    def opls_lj(self):
        """
        This function changes the standard OpenMM combination rules to use OPLS, execp and normal pairs are only
        required if their are virtual sites in the molecule.
        """
        forces = {self.system.getForce(index).__class__.__name__:self.system.getForce(index) for index in range(self.system.getNumForces())}
        nonbonded_force = forces['NonbondedForce']
        lorentz = mm.CustomNonbondedForce('epsilon*((sigma/r)^12-(sigma/r)^6); sigma=sqrt(sigma1*sigma2); epsilon=sqrt(epsilon1*epsilon2)*4.0')
        lorentz.setNonbondedMethod(nonbonded_force.getNonbondedMethod())
        lorentz.addPerParticleParameter('sigma')
        lorentz.addPerParticleParameter('epsilon')
        lorentz.setCutoffDistance(nonbonded_force.getCutoffDistance())
        self.system.addForce(lorentz)
        l_j_set = {}
        for index in range(nonbonded_force.getNumParticles()):
            charge, sigma, epsilon = nonbonded_force.getParticleParameters(index)
            l_j_set[index] = (sigma, epsilon, charge)
            lorentz.addParticle([sigma, epsilon])
            nonbonded_force.setParticleParameters(index, charge, 0, 0)

        for i in range(nonbonded_force.getNumExceptions()):
            p1, p2, q, sig, eps = nonbonded_force.getExceptionParameters(i)
            lorentz.addExclusion(p1, p2)
            if eps._value != 0.0:
                charge = 0.5 * (l_j_set[p1][2] * l_j_set[p2][2])
                sig14 = np.sqrt(l_j_set[p1][0] * l_j_set[p2][0])
                nonbonded_force.setExceptionParameters(i, p1, p2, charge, sig14, eps)

    @timer_logger
    def format_coords(self, coordinates):
        """
        Take the coordinates as a list and format to the OpenMM style of a list of tuples.
        :param coordinates: The flattened list of coordinates.
        :return: The OpenMM list of tuples.
        """
        coords = []
        for i in range(0, len(coordinates), 3):
            coords.append(tuple(coordinates[i:i + 3]))

        return coords

    @timer_logger
    def calculate_hessian(self, finite_step):
        """
        Using finite displacement calculate the hessian matrix of the molecule using symmetric difference quotient (SQD) rule.
        :param finite_step: The finite step size used in the calculation in nm
        :return: A numpy array of the mass weighted hessian of size 3N*3N
        """
        input_coords = self.molecule.coords['qm'].flatten() * constants.ANGS_TO_NM
        hessian = np.zeros((3 * len(self.molecule.atoms), 3 * len(self.molecule.atoms)))
        for i in range(3 * len(self.molecule.atoms)):
            for j in range(i, 3 * len(self.molecule.atoms)):
                if i == j:
                    coords = deepcopy(input_coords)
                    coords[i] += 2 * finite_step
                    e1 = self.get_energy(self.format_coords(coords))
                    coords = deepcopy(input_coords)
                    coords[i] -= 2 * finite_step
                    e2 = self.get_energy(self.format_coords(coords))
                    hessian[(i, j)] = (e1 + e2) / (4 * finite_step ** 2 * self.molecule.atoms[(i // 3)].atomic_mass)
                else:
                    coords = deepcopy(input_coords)
                    coords[i] += finite_step
                    coords[j] += finite_step
                    e1 = self.get_energy(self.format_coords(coords))
                    coords = deepcopy(input_coords)
                    coords[i] -= finite_step
                    coords[j] -= finite_step
                    e2 = self.get_energy(self.format_coords(coords))
                    coords = deepcopy(input_coords)
                    coords[i] += finite_step
                    coords[j] -= finite_step
                    e3 = self.get_energy(self.format_coords(coords))
                    coords = deepcopy(input_coords)
                    coords[i] -= finite_step
                    coords[j] += finite_step
                    e4 = self.get_energy(self.format_coords(coords))
                    hessian[(i, j)] = (e1 + e2 - e3 - e4) / (4 * finite_step ** 2 * self.molecule.atoms[(i // 3)].atomic_mass)

        sym_hessian = hessian + hessian.T - np.diag(hessian.diagonal())
        return sym_hessian

    @timer_logger
    def normal_modes(self, finite_step):
        """
        Calculate the normal modes of the molecule from the hessian matrix
        :param finite_step: The finite step size used in the calculation of the matrix
        :return: A numpy array of the normal modes of the molecule
        """
        hessian = self.calculate_hessian(finite_step)
        e_vals, e_vectors = np.linalg.eig(hessian)
        print(e_vals)
        print(e_vectors)
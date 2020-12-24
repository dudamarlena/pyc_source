# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/parametrisation/base_parametrisation.py
# Compiled at: 2019-09-23 09:51:08
# Size of source mod 2**32: 9634 bytes
from QUBEKit.utils import constants
from collections import OrderedDict
from copy import deepcopy
import xml.etree.ElementTree as ET

class Parametrisation:
    __doc__ = '\n    Class of methods which perform the initial parametrisation for the molecule.\n    The Parameters will be stored into the molecule as dictionaries as this is easy to manipulate and convert\n    to a parameter tree.\n\n    Note all parameters gathered here are indexed from 0,\n    whereas the ligand object indices start from 1 for all networkx related properties such as bonds!\n\n\n    Parameters\n    ---------\n    molecule : QUBEKit molecule object\n\n    input_file : an OpenMM style xml file associated with the molecule object\n\n    fftype : the FF type the molecule will be parametrised with\n             only needed in the case of gaff or gaff2 else will be assigned based on class used.\n\n    Returns\n    -------\n    AtomTypes : dictionary of the atom names, the associated OPLS type and class type stored under number.\n                {0: [C00, OPLS_800, C800]}\n\n    Residues : dictionary of residue names indexed by the order they appear.\n\n    HarmonicBondForce : dictionary of equilibrium distances and force constants stored under the bond tuple.\n                        {(0, 1): [eqr=456, fc=984375]}\n\n    HarmonicAngleForce : dictionary of equilibrium  angles and force constant stored under the angle tuple.\n\n    PeriodicTorsionForce : dictionary of periodicity, barrier and phase stored under the torsion tuple.\n\n    NonbondedForce : dictionary of charge, sigma and epsilon stored under the original atom ordering.\n    '

    def __init__(self, molecule, input_file=None, fftype=None):
        self.molecule = molecule
        self.input_file = input_file
        self.fftype = fftype
        self.molecule.combination = 'opls'
        self.combination = 'amber'
        self.molecule.AtomTypes = {}
        self.molecule.HarmonicBondForce = {bond:[0, 0] for bond in self.molecule.bond_lengths.keys()}
        self.molecule.HarmonicAngleForce = {angle:[0, 0] for angle in self.molecule.angle_values.keys()}
        self.molecule.NonbondedForce = OrderedDict(((number, [0, 0, 0]) for number in range(len(self.molecule.atoms))))
        self.molecule.PeriodicTorsionForce = OrderedDict()

    def __repr__(self):
        return f"{self.__class__.__name__}({self.__dict__!r})"

    def gather_parameters(self):
        """
        This method parses the serialised xml file and collects the parameters ready to pass them
        to build tree.
        """
        for atom in self.molecule.atoms:
            self.molecule.AtomTypes[atom.atom_index] = [
             atom.atom_name, 'QUBE_' + str(0 + atom.atom_index),
             str(atom.atomic_symbol) + str(0 + atom.atom_index)]

        phases = [0, constants.PI, 0, constants.PI]
        try:
            in_root = ET.parse('serialised.xml').getroot()
            for Bond in in_root.iter('Bond'):
                bond = (
                 int(Bond.get('p1')), int(Bond.get('p2')))
                if bond in self.molecule.HarmonicBondForce:
                    self.molecule.HarmonicBondForce[bond] = [
                     float(Bond.get('d')), float(Bond.get('k'))]
                else:
                    self.molecule.HarmonicBondForce[bond[::-1]] = [
                     float(Bond.get('d')), float(Bond.get('k'))]

            for Angle in in_root.iter('Angle'):
                angle = (
                 int(Angle.get('p1')), int(Angle.get('p2')), int(Angle.get('p3')))
                if angle in self.molecule.HarmonicAngleForce:
                    self.molecule.HarmonicAngleForce[angle] = [
                     float(Angle.get('a')), float(Angle.get('k'))]
                else:
                    self.molecule.HarmonicAngleForce[angle[::-1]] = [
                     float(Angle.get('a')), float(Angle.get('k'))]

            i = 0
            for Atom in in_root.iter('Particle'):
                if 'eps' in Atom.attrib:
                    self.molecule.NonbondedForce[i] = [
                     float(Atom.get('q')), float(Atom.get('sig')), float(Atom.get('eps'))]
                    i += 1

            for Torsion in in_root.iter('Torsion'):
                tor_str_forward = tuple((int(Torsion.get(f"p{i}")) for i in range(1, 5)))
                tor_str_back = tuple(reversed(tor_str_forward))
                if tor_str_forward not in self.molecule.PeriodicTorsionForce:
                    if tor_str_back not in self.molecule.PeriodicTorsionForce:
                        self.molecule.PeriodicTorsionForce[tor_str_forward] = [
                         [
                          int(Torsion.get('periodicity')), float(Torsion.get('k')), phases[(int(Torsion.get('periodicity')) - 1)]]]
                else:
                    if tor_str_forward in self.molecule.PeriodicTorsionForce:
                        self.molecule.PeriodicTorsionForce[tor_str_forward].append([
                         int(Torsion.get('periodicity')), float(Torsion.get('k')), phases[(int(Torsion.get('periodicity')) - 1)]])
                if tor_str_back in self.molecule.PeriodicTorsionForce:
                    self.molecule.PeriodicTorsionForce[tor_str_back].append([
                     int(Torsion.get('periodicity')), float(Torsion.get('k')), phases[(int(Torsion.get('periodicity')) - 1)]])

        except FileNotFoundError:
            if self.molecule.parameter_engine != 'none':
                raise FileNotFoundError('Molecule could not be serialised from OpenMM')

        if self.molecule.dihedrals is not None:
            for tor_list in self.molecule.dihedrals.values():
                for torsion in tor_list:
                    if torsion not in self.molecule.PeriodicTorsionForce and tuple(reversed(torsion)) not in self.molecule.PeriodicTorsionForce:
                        self.molecule.PeriodicTorsionForce[torsion] = [
                         [
                          1, 0, 0], [2, 0, constants.PI],
                         [
                          3, 0, 0], [4, 0, constants.PI]]

        torsions = [sorted(key) for key in self.molecule.PeriodicTorsionForce.keys()]
        if self.molecule.improper_torsions is not None:
            for torsion in self.molecule.improper_torsions:
                if sorted(torsion) not in torsions:
                    self.molecule.PeriodicTorsionForce[torsion] = [[1, 0, 0], [2, 0, constants.PI],
                     [
                      3, 0, 0], [4, 0, constants.PI]]

        for key, val in self.molecule.PeriodicTorsionForce.items():
            vns = [
             1, 2, 3, 4]
            if len(val) < 4:
                for force in val:
                    vns.remove(force[0])

                for i in vns:
                    val.append([i, 0, phases[(int(i) - 1)]])

        for val in self.molecule.PeriodicTorsionForce.values():
            val.sort(key=(lambda x: x[0]))

        improper_torsions = None
        if self.molecule.improper_torsions is not None:
            improper_torsions = OrderedDict()
            for improper in self.molecule.improper_torsions:
                for key, val in self.molecule.PeriodicTorsionForce.items():
                    if sorted(key) == sorted(improper):
                        self.molecule.PeriodicTorsionForce[key].append('Improper')
                        improper_torsions.setdefault(improper, []).append(val)

            for improper, params in improper_torsions.items():
                if len(params) != 1:
                    new_params = params[0]
                    for values in params[1:]:
                        for i in range(4):
                            new_params[i][1] += values[i][1]

                    improper_torsions[improper] = new_params
                else:
                    improper_torsions[improper] = params[0]

        torsions = deepcopy(self.molecule.PeriodicTorsionForce)
        self.molecule.PeriodicTorsionForce = OrderedDict(((v, k) for v, k in torsions.items() if k[(-1)] != 'Improper'))
        if improper_torsions is not None:
            for key, val in improper_torsions.items():
                self.molecule.PeriodicTorsionForce[key] = val
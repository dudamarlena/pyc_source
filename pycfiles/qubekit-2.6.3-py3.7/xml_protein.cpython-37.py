# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/parametrisation/xml_protein.py
# Compiled at: 2019-09-20 10:07:20
# Size of source mod 2**32: 6302 bytes
from QUBEKit.parametrisation.base_parametrisation import Parametrisation
from QUBEKit.utils.decorators import for_all_methods, timer_logger
from collections import OrderedDict
from copy import deepcopy
from simtk.openmm import app, XmlSerializer
import xml.etree.ElementTree as ET

@for_all_methods(timer_logger)
class XMLProtein(Parametrisation):
    __doc__ = 'Read in the parameters for a protein from the QUBEKit_general XML file and store them into the protein.'

    def __init__(self, protein, input_file='QUBE_general_pi.xml', fftype='CM1A/OPLS'):
        super().__init__(protein, input_file, fftype)
        self.serialise_system()
        self.gather_parameters()
        self.molecule.parameter_engine = 'XML input ' + self.fftype
        self.molecule.combination = 'opls'

    def serialise_system(self):
        """Serialise the input XML system using openmm."""
        pdb = app.PDBFile(self.molecule.filename)
        modeller = app.Modeller(pdb.topology, pdb.positions)
        forcefield = app.ForceField(self.input_file if self.input_file else f"{self.molecule.name}.xml")
        system = forcefield.createSystem((modeller.topology), nonbondedMethod=(app.NoCutoff), constraints=None)
        xml = XmlSerializer.serializeSystem(system)
        with open('serialised.xml', 'w+') as (out):
            out.write(xml)

    def gather_parameters(self):
        """This method parses the serialised xml file and collects the parameters ready to pass them
        to build tree.
        """
        for atom in self.molecule.atoms:
            self.molecule.AtomTypes[atom.atom_index] = [
             atom.name, f"QUBE_{atom.atom_index}", atom.name]

        input_xml_file = 'serialised.xml'
        in_root = ET.parse(input_xml_file).getroot()
        for Bond in in_root.iter('Bond'):
            self.molecule.HarmonicBondForce[(int(Bond.get('p1')), int(Bond.get('p2')))] = [
             Bond.get('d'), Bond.get('k')]

        self.molecule.update()
        for Angle in in_root.iter('Angle'):
            self.molecule.HarmonicAngleForce[(int(Angle.get('p1')), int(Angle.get('p2')), int(Angle.get('p3')))] = [
             Angle.get('a'), Angle.get('k')]

        i = 0
        for Atom in in_root.iter('Particle'):
            if 'eps' in Atom.attrib:
                self.molecule.NonbondedForce[i] = [
                 Atom.get('q'), Atom.get('sig'), Atom.get('eps')]
                i += 1

        phases = ['0', '3.141592653589793', '0', '3.141592653589793']
        for Torsion in in_root.iter('Torsion'):
            tor_string_forward = tuple((int(Torsion.get(f"p{i}")) for i in range(1, 5)))
            tor_string_back = tuple(reversed(tor_string_forward))
            if tor_string_forward not in self.molecule.PeriodicTorsionForce:
                if tor_string_back not in self.molecule.PeriodicTorsionForce:
                    self.molecule.PeriodicTorsionForce[tor_string_forward] = [
                     [
                      Torsion.get('periodicity'), Torsion.get('k'), phases[(int(Torsion.get('periodicity')) - 1)]]]
            else:
                if tor_string_forward in self.molecule.PeriodicTorsionForce:
                    self.molecule.PeriodicTorsionForce[tor_string_forward].append([
                     Torsion.get('periodicity'), Torsion.get('k'), phases[(int(Torsion.get('periodicity')) - 1)]])
            if tor_string_back in self.molecule.PeriodicTorsionForce:
                self.molecule.PeriodicTorsionForce[tor_string_back].append([
                 Torsion.get('periodicity'), Torsion.get('k'), phases[(int(Torsion.get('periodicity')) - 1)]])

        for tor_list in self.molecule.dihedrals.values():
            for torsion in tor_list:
                if torsion not in self.molecule.PeriodicTorsionForce and tuple(reversed(torsion)) not in self.molecule.PeriodicTorsionForce:
                    self.molecule.PeriodicTorsionForce[torsion] = [
                     [
                      '1', '0', '0'], ['2', '0', '3.141592653589793'],
                     [
                      '3', '0', '0'], ['4', '0', '3.141592653589793']]

        for key, val in self.molecule.PeriodicTorsionForce.items():
            vns = [
             '1', '2', '3', '4']
            if len(val) < 4:
                for force in val:
                    vns.remove(force[0])

                for i in vns:
                    val.append([i, '0', phases[(int(i) - 1)]])

        for force in self.molecule.PeriodicTorsionForce.values():
            force.sort(key=(lambda x: x[0]))

        improper_torsions = OrderedDict()
        for improper in self.molecule.improper_torsions:
            for key, val in self.molecule.PeriodicTorsionForce.items():
                if sorted(key) == sorted(improper):
                    self.molecule.PeriodicTorsionForce[key].append('Improper')
                    improper_torsions[improper] = val

        torsions = deepcopy(self.molecule.PeriodicTorsionForce)
        self.molecule.PeriodicTorsionForce = OrderedDict(((v, k) for v, k in torsions.items() if k[(-1)] != 'Improper'))
        for key, val in improper_torsions.items():
            self.molecule.PeriodicTorsionForce[key] = val
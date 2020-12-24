# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/parametrisation/openff.py
# Compiled at: 2019-09-23 09:51:08
# Size of source mod 2**32: 3763 bytes
from QUBEKit.parametrisation.base_parametrisation import Parametrisation
from QUBEKit.utils.decorators import for_all_methods, timer_logger
from openforcefield.topology import Molecule
from openforcefield.typing.engines.smirnoff import ForceField, BondHandler, AngleHandler, ProperTorsionHandler, vdWHandler
from openforcefield.typing.engines.smirnoff.parameters import UnassignedValenceParameterException
from simtk import unit
from simtk.openmm import XmlSerializer

@for_all_methods(timer_logger)
class OpenFF(Parametrisation):
    __doc__ = '\n    This class uses the openFFtoolkit 2 to parametrise a molecule and load an OpenMM simulation.\n    A serialised XML is then stored in the parameter dictionaries.\n    '

    def __init__(self, molecule, input_file=None, fftype='frost'):
        super().__init__(molecule, input_file, fftype)
        self.serialise_system()
        self.gather_parameters()
        self.molecule.parameter_engine = 'OpenFF_' + self.fftype
        self.molecule.combination = self.combination

    def serialise_system(self):
        """Create the OpenMM system; parametrise using frost; serialise the system."""
        off_molecule = Molecule.from_rdkit((self.molecule.rdkit_mol), allow_undefined_stereo=True)
        off_topology = off_molecule.to_topology()
        forcefield = ForceField('test_forcefields/smirnoff99Frosst.offxml')
        try:
            system = forcefield.create_openmm_system(off_topology)
        except (UnassignedValenceParameterException, TypeError, UnassignedValenceParameterException):
            new_bond = BondHandler.BondType(smirks='[*:1]~[*:2]', length='0 * angstrom', k='0.0 * angstrom**-2 * mole**-1 * kilocalorie')
            new_angle = AngleHandler.AngleType(smirks='[*:1]~[*:2]~[*:3]', angle='0.0 * degree', k='0.0 * mole**-1 * radian**-2 * kilocalorie')
            new_torsion = ProperTorsionHandler.ProperTorsionType(smirks='[*:1]~[*:2]~[*:3]~[*:4]',
              periodicity1='1',
              phase1='0.0 * degree',
              k1='0.0 * mole**-1 * kilocalorie',
              periodicity2='2',
              phase2='180.0 * degree',
              k2='0.0 * mole**-1 * kilocalorie',
              periodicity3='3',
              phase3='0.0 * degree',
              k3='0.0 * mole**-1 * kilocalorie',
              periodicity4='4',
              phase4='180.0 * degree',
              k4='0.0 * mole**-1 * kilocalorie',
              idivf1='1.0',
              idivf2='1.0',
              idivf3='1.0',
              idivf4='1.0')
            new_vdw = vdWHandler.vdWType(smirks='[*:1]', epsilon=(0 * unit.kilocalories_per_mole), sigma=(0 * unit.angstroms))
            new_generics = {'Bonds':new_bond,  'Angles':new_angle,  'ProperTorsions':new_torsion,  'vdW':new_vdw}
            for key, val in new_generics.items():
                forcefield.get_parameter_handler(key).parameters.insert(0, val)

            del forcefield._parameter_handlers['ToolkitAM1BCC']
            system = forcefield.create_openmm_system(off_topology)
            self.fftype = 'generics'

        with open('serialised.xml', 'w+') as (out):
            out.write(XmlSerializer.serializeSystem(system))
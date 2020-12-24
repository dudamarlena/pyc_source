# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/QUBEKit/protein_run.py
# Compiled at: 2019-07-30 08:48:15
# Size of source mod 2**32: 5061 bytes
from QUBEKit.ligand import Protein
from QUBEKit.parametrisation import XMLProtein
from QUBEKit.lennard_jones import LennardJones
from QUBEKit.protein_tools import qube_general, pdb_reformat, get_water
import argparse
from functools import partial
import os, sys
printf = partial(print, flush=True)

def main():
    """
    This script is used to prepare proteins with the QUBE FF
    1) prepare the protein for onetep using --setup which prints an xyz of the system
    2) after the onetep calculation bring back the ddec.onetep file and parametrise the system with --build
    this must be the same pdb used in setup as the atom order must be retained.
    """

    class SetupAction(argparse.Action):
        __doc__ = 'This class is called when we setup a new protein.'

        def __call__(self, pars, namespace, values, option_string=None):
            """This function is executed when setup is called."""
            printf('starting protein prep, reading pdb file...')
            protein = Protein(values)
            printf(f"{len(protein.Residues)} residues found!")
            protein.write_xyz(name='protein')
            printf('protein.xyz file made for ONETEP\n Run this file')
            sys.exit()

    class BuildAction(argparse.Action):
        __doc__ = 'This class handles the building of the protein xml and pdb files.'

        def __call__(self, pars, namespace, values, option_string=None):
            """This function is executed when build is called."""
            pro = Protein(values)
            qube_general()
            XMLProtein(pro)
            pro.charge = 0
            pro.charges_engine = 'onetep'
            pro.density_engine = 'onetep'
            lj = LennardJones(pro)
            pro.NonbondedForce = lj.calculate_non_bonded_force()
            printf('Writing pdb file with connections...')
            pro.write_pdb(name='QUBE_pro')
            printf('Writing XML file for the system...')
            pro.write_parameters(name='QUBE_pro', is_protein=True)
            os.remove('QUBE_general_pi.xml')
            printf('Done')
            sys.exit()

    class WaterAction(argparse.Action):
        __doc__ = 'This class builds the water models requested'

        def __call__(self, pars, namespace, values, option_string=None):
            """This function is executed when water is called."""
            get_water(values)
            sys.exit()

    class ConvertAction(argparse.Action):
        __doc__ = 'This class converts the names in a qube taj file to match the reference.'

        def __call__(self, pars, namespace, values, option_string=None):
            """This function is executed when water is called."""
            reference, target = values
            printf(reference, target)
            printf(f"Rewriting input: {target} to match: {reference}...")
            pdb_reformat(reference, target)
            printf('Done output made: QUBE_traj.pdb')
            sys.exit()

    parser = argparse.ArgumentParser(prog='QUBEKit-pro', formatter_class=(argparse.RawDescriptionHelpFormatter), description='QUBEKit-pro is an extension to QUBEKit that allows the preparationof amber prepared proteins with the QUBE forcefield and creates forcefield xml files for OpenMM simulation.')
    parser.add_argument('-setup', '--setup', action=SetupAction, help='Enter the name of the amber prepared protein file to convert to xyz for onetep.')
    parser.add_argument('-build', '--build_simulation_files', action=BuildAction, help='Enter the name of the amber prepared protein file to generate QUBE pdb and xml files.')
    parser.add_argument('-water', '--water', nargs='?', default='help', action=WaterAction, choices=[
     'help', 'tip3p', 'spce', 'tip4p', 'tip4pew', 'tip5p', 'tip3pfb', 'tip4pfb', 'tip4p-d',
     'opc'],
      help='Enter the name of the water model you would like to use.')
    parser.add_argument('-convert', '--convert', nargs=2, action=ConvertAction, help='Enter the reference followed by the qube traj file you want to re format.')
    parser.parse_args()


if __name__ == '__main__':
    main()
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/OpenDiscovery/lib/prepare_ligand4.py
# Compiled at: 2013-03-29 21:19:59
import os
from MolKit import Read
from AutoDockTools.MoleculePreparation import AD4LigandPreparation
if __name__ == '__main__':
    import sys, getopt

    def usage():
        """Print helpful, accurate usage statement to stdout."""
        print 'Usage: prepare_ligand4.py -l filename'
        print
        print '    Description of command...'
        print '         -l     ligand_filename (.pdb or .mol2 or .pdbq format)'
        print '    Optional parameters:'
        print '        [-v]    verbose output'
        print '        [-o pdbqt_filename] (default output filename is ligand_filename_stem + .pdbqt)'
        print '        [-d]    dictionary to write types list and number of active torsions '
        print '        [-A]    type(s) of repairs to make:\n\t\t bonds_hydrogens, bonds, hydrogens (default is to do no repairs)'
        print '        [-C]    do not add charges (default is to add gasteiger charges)'
        print '        [-p]    preserve input charges on atom type, eg -p Zn'
        print '               (default is not to preserve charges on any specific atom type)'
        print "        [-U]    cleanup type:\n\t\t nphs_lps, nphs, lps, '' (default is 'nphs_lps') "
        print '        [-B]    type(s) of bonds to allow to rotate '
        print "               (default sets 'backbone' rotatable and 'amide' + 'guanidinium' non-rotatable)"
        print '        [-R]    index for root'
        print '        [-F]    check for and use largest non-bonded fragment (default is not to do this)'
        print '        [-M]    interactive (default is automatic output)'
        print '        [-I]    string of bonds to inactivate composed of '
        print '                   of zero-based atom indices eg 5_13_2_10  '
        print '                   will inactivate atoms[5]-atoms[13] bond '
        print '                               and atoms[2]-atoms[10] bond '
        print '                      (default is not to inactivate any specific bonds)'
        print '        [-Z]    inactivate all active torsions     '
        print '                      (default is leave all rotatable active except amide and guanidinium)'
        print '        [-g]    attach all nonbonded fragments '
        print '        [-s]    attach all nonbonded singletons: '
        print '                   NB: sets attach all nonbonded fragments too'
        print '                      (default is not to do this)'


    try:
        opt_list, args = getopt.getopt(sys.argv[1:], 'l:vo:d:A:Cp:U:B:R:MFI:Zgsh')
    except getopt.GetoptError as msg:
        print 'prepare_ligand4.py: %s' % msg
        usage()
        sys.exit(2)

    ligand_filename = None
    verbose = None
    add_bonds = False
    repairs = ''
    charges_to_add = 'gasteiger'
    preserve_charge_types = ''
    cleanup = 'nphs_lps'
    allowed_bonds = 'backbone'
    root = 'auto'
    outputfilename = None
    check_for_fragments = False
    bonds_to_inactivate = ''
    inactivate_all_torsions = False
    attach_nonbonded_fragments = False
    attach_singletons = False
    mode = 'automatic'
    dict = None
    for o, a in opt_list:
        if o in ('-l', '--l'):
            ligand_filename = a
            if verbose:
                print 'set ligand_filename to ', a
        if o in ('-v', '--v'):
            verbose = True
            if verbose:
                print 'set verbose to ', True
        if o in ('-o', '--o'):
            outputfilename = a
            if verbose:
                print 'set outputfilename to ', a
        if o in ('-d', '--d'):
            dict = a
            if verbose:
                print 'set dict to ', a
        if o in ('-A', '--A'):
            repairs = a
            if verbose:
                print 'set repairs to ', a
        if o in ('-C', '--C'):
            charges_to_add = None
            if verbose:
                print 'do not add charges'
        if o in ('-p', '--p'):
            preserve_charge_types += a
            preserve_charge_types += ','
            if verbose:
                print 'preserve initial charges on ', preserve_charge_types
        if o in ('-U', '--U'):
            cleanup = a
            if verbose:
                print 'set cleanup to merge ', a
        if o in ('-B', '--B'):
            allowed_bonds = a
            if verbose:
                print 'allow ', a, 'bonds set to rotate'
        if o in ('-R', '--R'):
            root = a
            if verbose:
                print 'set root to ', root
        if o in ('-F', '--F'):
            check_for_fragments = True
            if verbose:
                print 'set check_for_fragments to True'
        if o in ('-M', '--M'):
            mode = a
            if verbose:
                print 'set mode to ', a
        if o in ('-I', '--I'):
            bonds_to_inactivate = a
            if verbose:
                print 'set bonds_to_inactivate to ', a
        if o in ('-Z', '--Z'):
            inactivate_all_torsions = True
            if verbose:
                print 'set inactivate_all_torsions to ', inactivate_all_torsions
        if o in ('-g', '--g'):
            attach_nonbonded_fragments = True
            if verbose:
                print 'set attach_nonbonded_fragments to ', attach_nonbonded_fragments
        if o in ('-s', '--s'):
            attach_singletons = True
            if verbose:
                print 'set attach_singletons to ', attach_singletons
        if o in ('-h', '--'):
            usage()
            sys.exit()

    if not ligand_filename:
        print 'prepare_ligand4: ligand filename must be specified.'
        usage()
        sys.exit()
    if attach_singletons:
        attach_nonbonded_fragments = True
        if verbose:
            print 'using attach_singletons so attach_nonbonded_fragments also'
    mols = Read(ligand_filename)
    if verbose:
        print 'read ', ligand_filename
    mol = mols[0]
    if len(mols) > 1:
        if verbose:
            print 'more than one molecule in file'
        ctr = 1
        for m in mols[1:]:
            ctr += 1
            if len(m.allAtoms) > len(mol.allAtoms):
                mol = m
                if verbose:
                    print 'mol set to ', ctr, 'th molecule with', len(mol.allAtoms), 'atoms'

    coord_dict = {}
    for a in mol.allAtoms:
        coord_dict[a] = a.coords

    mol.buildBondsByDistance()
    if charges_to_add is not None:
        preserved = {}
        preserved_types = preserve_charge_types.split(',')
        for t in preserved_types:
            if not len(t):
                continue
            ats = mol.allAtoms.get(lambda x: x.autodock_element == t)
            for a in ats:
                if a.chargeSet is not None:
                    preserved[a] = [
                     a.chargeSet, a.charge]

    if verbose:
        print 'setting up LPO with mode=', mode,
        print 'and outputfilename= ', outputfilename
        print 'and check_for_fragments=', check_for_fragments
        print 'and bonds_to_inactivate=', bonds_to_inactivate
    LPO = AD4LigandPreparation(mol, mode, repairs, charges_to_add, cleanup, allowed_bonds, root, outputfilename=outputfilename, dict=dict, check_for_fragments=check_for_fragments, bonds_to_inactivate=bonds_to_inactivate, inactivate_all_torsions=inactivate_all_torsions, attach_nonbonded_fragments=attach_nonbonded_fragments, attach_singletons=attach_singletons)
    if charges_to_add is not None:
        for atom, chargeList in preserved.items():
            atom._charges[chargeList[0]] = chargeList[1]
            atom.chargeSet = chargeList[0]

    if verbose:
        print 'returning ', mol.returnCode
    bad_list = []
    for a in mol.allAtoms:
        if a in coord_dict.keys() and a.coords != coord_dict[a]:
            bad_list.append(a)

    if len(bad_list):
        print len(bad_list), ' atom coordinates changed!'
        for a in bad_list:
            print a.name, ':', coord_dict[a], ' -> ', a.coords

    elif verbose:
        print 'No change in atomic coordinates'
    if mol.returnCode != 0:
        sys.stderr.write(mol.returnMsg + '\n')
    sys.exit(mol.returnCode)
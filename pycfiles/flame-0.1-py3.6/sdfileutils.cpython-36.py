# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/chem/sdfileutils.py
# Compiled at: 2018-05-22 12:10:29
# Size of source mod 2**32: 4277 bytes
import os
from rdkit import Chem

def count_mols(ifile):
    return len(Chem.SDMolSupplier(ifile))


def split_SDFile(ifile, num_chunks):
    """
    Splits the input SDfile in pieces SDfiles files of balanced size.
    Every file is named "filename_0.sdf", "filename_1.sdf", ...

    Argument:
        ifile       : input SDfile
        num_chunks  : number of pieces

    Output:
        list of split file names
        list of number of molecules within each file
    """
    suppl = Chem.SDMolSupplier(ifile)
    num_mols = len(suppl)
    if num_mols == 0:
        return (False, 'No molecule found in file: ' + ifile)
    else:
        if num_chunks < 2:
            return (True, ([ifile], [num_mols]))
        chunk_size = num_mols // num_chunks
        filename, fileext = os.path.splitext(ifile)
        temp_files_name = []
        temp_files_size = []
        chunk_i = 0
        chunk_mol_i = 0
        chunk_name = '{}_{}{}'.format(filename, chunk_i, fileext)
        fo = open(chunk_name, 'w', newline='\n')
        temp_files_name.append(chunk_name)
        for mi in range(num_mols):
            if mi // chunk_size > chunk_i:
                if chunk_i < num_chunks - 1:
                    fo.close()
                    temp_files_size.append(chunk_mol_i)
                    chunk_i += 1
                    chunk_mol_i = 0
                    chunk_name = '{}_{}{}'.format(filename, chunk_i, fileext)
                    fo = open(chunk_name, 'w', newline='\n')
                    temp_files_name.append(chunk_name)
            fo.write(suppl.GetItemText(mi))
            chunk_mol_i += 1

        fo.close()
        temp_files_size.append(chunk_mol_i)
        return (
         True, (temp_files_name, temp_files_size))


def getNameFromEmpty(suppl, count=1, field=None):
    molText = suppl.GetItemText(count)
    name = ''
    if field is not None:
        fieldName = '> <%s>' % field
        found = False
        for line in molText.split('\n'):
            if line.rstrip() == fieldName:
                found = True
                continue
                if found:
                    name = line.rstrip()
                    break

    else:
        name = molText.split('\n')[0].rstrip()
    if name == '':
        name = 'mol%0.10d' % count
    if ' ' in name:
        name = name.replace(' ', '_')
    return name


def getName(mol, count=1, field=None, suppl=None):
    if not mol:
        if suppl:
            name = getNameFromEmpty(suppl, count, field)
    else:
        name = ''
        candidates = []
        if field:
            if isinstance(field, list):
                candidates = field
            elif isinstance(field, str):
                candidates = [
                 field]
        candidates.append('_Name')
        for iname in candidates:
            if mol.HasProp(iname):
                name = mol.GetProp(iname)
                break

        if name == '':
            name = 'mol%0.10d' % count
    if ' ' in name:
        name = name.replace(' ', '_')
    return name
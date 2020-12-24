# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flame/chem/compute_md.py
# Compiled at: 2018-06-18 07:55:18
# Size of source mod 2**32: 6677 bytes
import os, shutil, tempfile, requests, numpy as np
from rdkit import Chem
from rdkit.Chem import rdMolDescriptors
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors

def _RDKit_properties(ifile):
    """ 
    computes RDKit properties for the file provided as argument

    output is a boolean and a tupla with the xmatrix and the variable names

    """
    try:
        suppl = Chem.SDMolSupplier(ifile)
    except:
        return (False, 'unable to compute RDKit properties')
    else:
        properties = rdMolDescriptors.Properties()
        md_nam = []
        success_list = []
        xmatrix = []
        for nam in properties.GetPropertyNames():
            md_nam.append(nam)

        try:
            num_obj = 0
            for mol in suppl:
                if mol is None:
                    print('ERROR: (@_RDKit_properties) Unable to process molecule #', str(num_obj + 1), 'in file ' + ifile)
                    success_list.append(False)
                else:
                    if num_obj == 0:
                        xmatrix = properties.ComputeProperties(mol)
                    else:
                        xmatrix = np.vstack((
                         xmatrix, properties.ComputeProperties(mol)))
                    success_list.append(True)
                    num_obj += 1

        except:
            return (
             False, 'Failed computing RDKit properties for molecule' + str(num_obj + 1) + 'in file ' + ifile)
        else:
            if num_obj == 0:
                return (False, 'Unable to compute RDKit properties for molecule ' + ifile)
            else:
                return (
                 True, (xmatrix, md_nam, success_list))


def _RDKit_descriptors(ifile):
    """ 
    computes RDKit descriptors for the file provided as argument

    output is a boolean and a tupla with the xmatrix and the variable names

    """
    try:
        suppl = Chem.SDMolSupplier(ifile)
    except:
        return (False, 'Unable to compute RDKit MD')
    else:
        nms = [x[0] for x in Descriptors._descList]
        md = MoleculeDescriptors.MolecularDescriptorCalculator(nms)
        success_list = []
        xmatrix = []
        try:
            num_obj = 0
            for mol in suppl:
                if mol is None:
                    print('ERROR: (@_RDKit_descriptors) Unable to process molecule #', str(num_obj + 1), 'in file ' + ifile)
                    success_list.append(False)
                else:
                    if num_obj == 0:
                        xmatrix = md.CalcDescriptors(mol)
                    else:
                        xmatrix = np.vstack((xmatrix, md.CalcDescriptors(mol)))
                    success_list.append(True)
                    num_obj += 1

        except:
            return (
             False, 'Failed computing RDKit descriptors for molecule' + str(num_obj + 1) + 'in file ' + ifile)
        else:
            if num_obj == 0:
                return (False, 'Unable to compute RDKit properties for molecule ' + ifile)
            else:
                if num_obj == 0:
                    return (False, 'Unable to compute RDKit descriptors for molecule ' + ifile)
                return (True, (xmatrix, nms, success_list))


def _padel_descriptors(ifile):
    """ 
    computes Padel molecular descriptors calling an external web service for
    the file provided as argument

    output is a boolean and a tupla with the xmatrix and the variable names

    """
    uri = 'http://localhost:5000/padel/api/v0.1/calc/json'
    tmpdir = os.path.abspath(tempfile.mkdtemp(dir=(os.path.dirname(ifile))))
    shutil.copy(ifile, tmpdir)
    payload = {'-2d':'', 
     '-dir':tmpdir}
    try:
        req = requests.post(uri, json=payload)
        if req.status_code != 200:
            return (
             False, 'ERROR: failed to contact padel service with code: ' + str(req.status_code))
    except:
        return (False, 'ERROR: failed to contact padel service')
        print('padel service results : ', req.json())
        results = req.json()
        return results['success'] or (False, 'padel service returned error condition')
    else:
        ofile = os.path.join(tmpdir, results['filename'])
        if not os.path.isfile(ofile):
            return (False, 'padel service returned no file')
        else:
            with open(ofile, 'r') as (of):
                index = 0
                var_nam = []
                success_list = []
                xmatrix = []
                for line in of:
                    if index == 0:
                        var_nam = line.strip().split(',')
                        var_nam = var_nam[1:]
                    else:
                        value_list = line.strip().split(',')
                        try:
                            nvalue_list = [float(x) for x in value_list[1:]]
                        except:
                            success_list.append(False)
                            print('ERROR (@_padel_descriptors) in Padel results parsing for object ' + str(index))
                            continue

                        md = np.array(nvalue_list, dtype=(np.float64))
                        if index == 1:
                            xmatrix = md
                        else:
                            xmatrix = np.vstack((xmatrix, md))
                        success_list.append(True)
                    index += 1

            shutil.rmtree(tmpdir)
            return (
             index > 1, (xmatrix, var_nam, success_list))
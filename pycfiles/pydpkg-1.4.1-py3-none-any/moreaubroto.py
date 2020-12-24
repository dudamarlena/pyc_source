# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/orient/pydpi/src/pydpi/drug/moreaubroto.py
# Compiled at: 2012-09-19 09:04:03
__doc__ = '\n##############################################################################\n\nThe calculation of Moreau-Broto autocorrelation descriptors. You can get 32\n\nmolecular decriptors. You can freely use and distribute it. If you hava  \n\nany problem, you could contact with us timely!\n\nAuthors: Dongsheng Cao and Yizeng Liang.\n\nDate: 2012.09.18\n\nEmail: oriental-cds@163.com\n\n##############################################################################\n'
from rdkit import Chem
from AtomProperty import GetRelativeAtomicProperty
import numpy
Version = 1.0

def _CalculateMoreauBrotoAutocorrelation(mol, lag=1, propertylabel='m'):
    """
    #################################################################
    **Internal used only**
    
    Calculation of Moreau-Broto autocorrelation descriptors based on 
    
    different property weights.
    
    Usage:
    
    res=_CalculateMoreauBrotoAutocorrelation(mol, lag=1,propertylabel='m')
    
    Input: mol is a molecule object.
    
    lag is the topological distance between atom i and atom j.
    
    propertylabel is the weighted property.
    
    Output: res is a numeric value.
    #################################################################
    """
    Natom = mol.GetNumAtoms()
    GetDistanceMatrix = Chem.GetDistanceMatrix(mol)
    res = 0.0
    for i in range(Natom):
        for j in range(Natom):
            if GetDistanceMatrix[(i, j)] == lag:
                atom1 = mol.GetAtomWithIdx(i)
                atom2 = mol.GetAtomWithIdx(j)
                temp1 = GetRelativeAtomicProperty(element=atom1.GetSymbol(), propertyname=propertylabel)
                temp2 = GetRelativeAtomicProperty(element=atom2.GetSymbol(), propertyname=propertylabel)
                res = res + temp1 * temp2
            else:
                res = res + 0.0

    return round(numpy.log(res / 2 + 1), 3)


def CalculateMoreauBrotoAutoMass(mol):
    """
    #################################################################
    Calculation of Moreau-Broto autocorrelation descriptors based on 
    
    carbon-scaled atomic mass.
    
    Usage:
    
    res=CalculateMoreauBrotoAutoMass(mol)
    
    Input: mol is a molecule object.
    
    Output: res is a dict form containing eight moreau broto autocorrealtion
    
    descriptors.
    #################################################################
    """
    res = {}
    for i in range(8):
        res['ATSm' + str(i + 1)] = _CalculateMoreauBrotoAutocorrelation(mol, lag=i + 1, propertylabel='m')

    return res


def CalculateMoreauBrotoAutoVolume(mol):
    """
    #################################################################
    Calculation of Moreau-Broto autocorrelation descriptors based on 
    
    carbon-scaled atomic van der Waals volume.
    
    Usage: 
    
    res=CalculateMoreauBrotoAutoVolume(mol)
    
    Input: mol is a molcule object.
    
    Output: res is a dict form containing eight moreau broto autocorrealtion
    
    descriptors.
    #################################################################
    """
    res = {}
    for i in range(8):
        res['ATSv' + str(i + 1)] = _CalculateMoreauBrotoAutocorrelation(mol, lag=i + 1, propertylabel='V')

    return res


def CalculateMoreauBrotoAutoElectronegativity(mol):
    """
    #################################################################
    Calculation of Moreau-Broto autocorrelation descriptors based on 
    
    carbon-scaled atomic Sanderson electronegativity.

    Usage: 
    
    res=CalculateMoreauBrotoAutoElectronegativity(mol)
    
    Input: mol is a molcule object.
    
    Output: res is a dict form containing eight moreau broto autocorrealtion
    
    descriptors.
    #################################################################
    """
    res = {}
    for i in range(8):
        res['ATSe' + str(i + 1)] = _CalculateMoreauBrotoAutocorrelation(mol, lag=i + 1, propertylabel='En')

    return res


def CalculateMoreauBrotoAutoPolarizability(mol):
    """
    #################################################################
    Calculation of Moreau-Broto autocorrelation descriptors based on 
    
    carbon-scaled atomic polarizability.

    res=CalculateMoreauBrotoAutoPolarizability(mol)
    
    Input: mol is a molcule object.
    
    Output: res is a dict form containing eight moreau broto autocorrealtion
    
    descriptors.
    #################################################################
    """
    res = {}
    for i in range(8):
        res['ATSp' + str(i + 1)] = _CalculateMoreauBrotoAutocorrelation(mol, lag=i + 1, propertylabel='alapha')

    return res


def GetMoreauBrotoAuto(mol):
    """
    #################################################################
    Calcualate all Moreau-Broto autocorrelation descriptors. 
    
    (carbon-scaled atomic mass, carbon-scaled atomic van der Waals volume,
     
    carbon-scaled atomic Sanderson electronegativity,
     
    carbon-scaled atomic polarizability)
    
    Usage:
    
    res=GetMoreauBrotoAuto(mol)
    
    Input: mol is a molecule object.
    
    Output: res is a dict form containing all moreau broto autocorrelation
    
    descriptors.
    #################################################################
    """
    res = {}
    res.update(CalculateMoreauBrotoAutoMass(mol))
    res.update(CalculateMoreauBrotoAutoVolume(mol))
    res.update(CalculateMoreauBrotoAutoElectronegativity(mol))
    res.update(CalculateMoreauBrotoAutoPolarizability(mol))
    return res


if __name__ == '__main__':
    smi5 = [
     'COCCCC', 'CCC(C)CC', 'CC(C)CCC', 'CC(C)C(C)C', 'CCOCCN', 'c1ccccc1N']
    smis = ['CCCC', 'CCCCC', 'CCCCCC', 'CC(N)C(=O)O', 'CC(N)C(=O)[O-].[Na+]']
    for index, smi in enumerate(smis):
        m = Chem.MolFromSmiles(smi)
        print index + 1
        print smi
        print len(GetMoreauBrotoAuto(m))
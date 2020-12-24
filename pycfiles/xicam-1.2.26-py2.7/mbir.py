# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\tomography\mbir.py
# Compiled at: 2018-08-27 17:21:07
__author__ = 'Luis Barroso-Luque, Holden Parks'
__copyright__ = 'Copyright 2016, CAMERA, LBL, ALS'
__credits__ = ['Ronald J Pandolfi', 'Dinesh Kumar', 'Singanallur Venkatakrishnan', 'Luis Luque',
 'Holden Parks', 'Alexander Hexemer']
__license__ = ''
__version__ = '1.2.1'
__maintainer__ = 'Ronald J Pandolfi'
__email__ = 'ronpandolfi@lbl.gov'
__status__ = 'Beta'
from tomocam import tomoCam

def recon(tomo, theta, center=None, algorithm=None, input_params=None, **kwargs):
    """
    Wrapper for TomoCam reconstruction functions

    Parameters
    ----------
    tomo : np.ndarray
        3D tomography data
    theta : list
        List of angles at which tomography data was taken
    center : float, optional
        Center of rotation of dataset
    algorithm : str, optional
        Name of algorithm to be run (either 'gridrec' or 'sirt'
    input_params : dict, optional
        Dictionary of other params for reconstruction
    """
    if 'gridrec' in algorithm:
        return tomoCam.gpuGridrec(tomo, theta, center, input_params)
    if 'sirt' in algorithm:
        return tomoCam.gpuSIRT(tomo, theta, center, input_params)
    raise ValueError("TomoCam reconstruction must be either 'gridrec', 'sirt', or 'mbir'")
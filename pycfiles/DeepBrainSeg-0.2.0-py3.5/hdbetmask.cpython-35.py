# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepBrainSeg/brainmask/hdbetmask.py
# Compiled at: 2019-11-11 08:44:10
# Size of source mod 2**32: 1043 bytes
import os, numpy as np, nibabel as nib, sys

def get_bet_mask(vol_path, save_path, device=0):
    """
                We make use of ants framework for generalized skull stripping
                
                t1_path: t1 volume path (str)
                saves the mask in the same location as t1 data directory
                returns: maskvolume (numpy uint8 type) 
        """
    print(save_path)
    filename = vol_path.split('/').pop().split('.')[0]
    os.system('hd-bet -i ' + vol_path + ' -device ' + str(device) + ' -mode fast -tta 0')
    os.makedirs(save_path, exist_ok=True)
    os.system('mv ' + os.path.join(os.path.dirname(vol_path), filename + '_bet.nii.gz') + ' ' + os.path.join(save_path, filename + '.nii.gz'))
    os.system('mv ' + os.path.join(os.path.dirname(vol_path), filename + '_bet_mask.nii.gz') + ' ' + os.path.join(save_path, filename + '_mask.nii.gz'))
    volume = np.uint8(nib.load(os.path.join(save_path, filename + '_mask.nii.gz')).get_data())
    return volume
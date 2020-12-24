# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/DeepBrainSeg/brainmask/antsmask.py
# Compiled at: 2019-11-11 08:44:10
# Size of source mod 2**32: 1320 bytes
import os, numpy as np, nibabel as nib

def get_ants_mask(t1_path, save_path, ants_path='/opt/ANTs/bin/'):
    """
                We make use of ants framework for generalized skull stripping
                
                t1_path: t1 volume path (str)
                saves the mask in the same location as t1 data directory
                returns: maskvolume (numpy uint8 type) 
        """
    mask_path = os.path.join(os.path.dirname(t1_path), 'mask.nii.gz')
    os.system(ants_path + 'ImageMath 3 ' + mask_path + ' Normalize ' + t1_path)
    os.system(ants_path + 'ThresholdImage 3 ' + mask_path + ' ' + mask_path + ' 0.01 1')
    os.system(ants_path + 'ImageMath 3 ' + mask_path + ' MD ' + mask_path + ' 1')
    os.system(ants_path + 'ImageMath 3 ' + mask_path + ' ME ' + mask_path + ' 1')
    os.system(ants_path + 'CopyImageHeaderInformation ' + t1_path + ' ' + mask_path + ' ' + mask_path + ' 1 1 1')
    mask = np.uint8(nib.load(mask_path).get_data())
    os.makedirs(os.path.basename(save_path), exist_ok=True)
    nib_obj = nib.load(t1_path)
    vol = nib_obj.get_data()
    affine = nib_obj.affine
    print(save_path)
    volume = np.uint8(vol * mask)
    volume = nib.Nifti1Image(volume, affine)
    volume.set_data_dtype(np.uint8)
    nib.save(volume, save_path)
    return mask
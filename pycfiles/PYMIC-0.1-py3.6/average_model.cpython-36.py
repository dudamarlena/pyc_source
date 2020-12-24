# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/util/average_model.py
# Compiled at: 2019-12-07 03:31:59
# Size of source mod 2**32: 895 bytes
import torch
checkpoint_name1 = '/home/guotai/projects/PyMIC/examples/brats/model/casecade/wt/unet3d_4_8000.pt'
checkpoint1 = torch.load(checkpoint_name1)
state_dict1 = checkpoint1['model_state_dict']
checkpoint_name2 = '/home/guotai/projects/PyMIC/examples/brats/model/casecade/wt/unet3d_4_10000.pt'
checkpoint2 = torch.load(checkpoint_name2)
state_dict2 = checkpoint2['model_state_dict']
checkpoint_name3 = '/home/guotai/projects/PyMIC/examples/brats/model/casecade/wt/unet3d_4_12000.pt'
checkpoint3 = torch.load(checkpoint_name3)
state_dict3 = checkpoint3['model_state_dict']
state_dict = {}
for item in state_dict1:
    print(item)
    state_dict[item] = (state_dict1[item] + state_dict2[item] + state_dict3[item]) / 3

save_dict = {'model_state_dict': state_dict}
save_name = '/home/guotai/projects/PyMIC/examples/brats/model/casecade/wt/unet3d_4_avg.pt'
torch.save(save_dict, save_name)
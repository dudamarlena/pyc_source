# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/train_infer/net_factory.py
# Compiled at: 2020-04-15 21:24:26
# Size of source mod 2**32: 453 bytes
from __future__ import print_function, division
from pymic.net2d.unet2d import UNet2D
from pymic.net2d.unet2d_scse import UNet2D_ScSE
from pymic.net3d.unet2d5 import UNet2D5
from pymic.net3d.unet3d import UNet3D
net_dict = {'UNet2D':UNet2D, 
 'UNet2D_ScSE':UNet2D_ScSE, 
 'UNet2D5':UNet2D5, 
 'UNet3D':UNet3D}

def get_network(params):
    net_type = params['net_type']
    net = net_dict[net_type](params)
    return net
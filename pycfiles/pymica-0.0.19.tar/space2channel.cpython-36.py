# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/layer/space2channel.py
# Compiled at: 2019-12-07 03:31:58
# Size of source mod 2**32: 3181 bytes
from __future__ import print_function, division
import numpy as np, torch, torch.nn as nn, SimpleITK as sitk

class SpaceToChannel3D(nn.Module):

    def __init__(self):
        super(SpaceToChannel3D, self).__init__()

    def forward(self, x):
        input_shape = list(x.shape)
        if not len(input_shape) == 5:
            raise AssertionError
        else:
            B, C, D, H, W = input_shape
            assert D % 2 == 0 and H % 2 == 0 and W % 2 == 0
        halfD = int(D / 2)
        halfH = int(H / 2)
        halfW = int(W / 2)
        x1 = x.contiguous().view([B, C, halfD, 2, H, W])
        x2 = x1.permute(0, 1, 3, 2, 4, 5)
        x3 = x2.contiguous().view([B, C * 2, halfD, halfH, 2, W])
        x4 = x3.permute(0, 1, 4, 2, 3, 5)
        x5 = x4.contiguous().view([B, C * 4, halfD, halfH, halfW, 2])
        x6 = x5.permute(0, 1, 5, 2, 3, 4)
        x7 = x6.contiguous().view([B, C * 8, halfD, halfH, halfW])
        return x7


class ChannelToSpace3D(nn.Module):

    def __init__(self):
        super(ChannelToSpace3D, self).__init__()

    def forward(self, x):
        input_shape = list(x.shape)
        if not len(input_shape) == 5:
            raise AssertionError
        else:
            B, C, D, H, W = input_shape
            assert C % 8 == 0
        Cd8 = int(C / 8)
        Cd4 = 2 * Cd8
        Cd2 = 2 * Cd4
        x6 = x.contiguous().view([B, Cd2, 2, D, H, W])
        x5 = x6.permute(0, 1, 3, 4, 5, 2)
        x4 = x5.contiguous().view([B, Cd4, 2, D, H, 2 * W])
        x3 = x4.permute(0, 1, 3, 4, 2, 5)
        x2 = x3.contiguous().view([B, Cd8, 2, D, 2 * H, 2 * W])
        x1 = x2.permute(0, 1, 3, 2, 4, 5)
        x0 = x1.contiguous().view([B, Cd8, 2 * D, 2 * H, 2 * W])
        return x0


if __name__ == '__main__':
    s2c = SpaceToChannel3D()
    s2c = s2c.double()
    c2s = ChannelToSpace3D()
    c2s = c2s.double()
    img_name = '/home/disk2t/data/brats/BraTS2018_Training/HGG/Brats18_2013_2_1/Brats18_2013_2_1_flair.nii.gz'
    img_obj = sitk.ReadImage(img_name)
    img_data = sitk.GetArrayFromImage(img_obj)
    img_data = img_data[:-1]
    print(img_data.shape)
    x = img_data.reshape([1, 1] + list(img_data.shape))
    xt = torch.from_numpy(x)
    xt = torch.tensor(xt)
    y = s2c(xt)
    z = c2s(y)
    y = y.detach().numpy()[0]
    print(y.shape)
    for i in range(8):
        sub_img = sitk.GetImageFromArray(y[i])
        save_name = '../../temp/{0:}.nii.gz'.format(i)
        sitk.WriteImage(sub_img, save_name)

    z = z.detach().numpy()[0]
    print(z.shape)
    rec_img = sitk.GetImageFromArray(z[0])
    save_name = '../../temp/rec.nii.gz'
    sitk.WriteImage(rec_img, save_name)
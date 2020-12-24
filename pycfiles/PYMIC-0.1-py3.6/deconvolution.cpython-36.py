# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pymic/layer/deconvolution.py
# Compiled at: 2020-04-15 21:24:26
# Size of source mod 2**32: 3524 bytes
from __future__ import print_function, division
import torch, torch.nn as nn

class DeconvolutionLayer(nn.Module):
    __doc__ = '\n    A compose layer with the following components:\n    deconvolution -> (batch_norm) -> activation -> (dropout)\n    batch norm and dropout are optional\n    '

    def __init__(self, in_channels, out_channels, kernel_size, dim=3, stride=1, padding=0, output_padding=0, dilation=1, groups=1, bias=True, batch_norm=True, acti_func=None):
        super(DeconvolutionLayer, self).__init__()
        self.n_in_chns = in_channels
        self.n_out_chns = out_channels
        self.batch_norm = batch_norm
        self.acti_func = acti_func
        if not dim == 2:
            if not dim == 3:
                raise AssertionError
        if dim == 2:
            self.conv = nn.ConvTranspose2d(in_channels, out_channels, kernel_size, stride, padding, output_padding, groups, bias, dilation)
            if self.batch_norm:
                self.bn = nn.BatchNorm2d(out_channels)
        else:
            self.conv = nn.ConvTranspose3d(in_channels, out_channels, kernel_size, stride, padding, output_padding, groups, bias, dilation)
        if self.batch_norm:
            self.bn = nn.BatchNorm3d(out_channels)

    def forward(self, x):
        f = self.conv(x)
        if self.batch_norm:
            f = self.bn(f)
        if self.acti_func is not None:
            f = self.acti_func(f)
        return f


class DepthSeperableDeconvolutionLayer(nn.Module):
    __doc__ = '\n    A compose layer with the following components:\n    convolution -> (batch_norm) -> activation -> (dropout)\n    batch norm and dropout are optional\n    '

    def __init__(self, in_channels, out_channels, kernel_size, dim=3, stride=1, padding=0, output_padding=0, dilation=1, groups=1, bias=True, batch_norm=True, acti_func=None):
        super(DepthSeperableDeconvolutionLayer, self).__init__()
        self.n_in_chns = in_channels
        self.n_out_chns = out_channels
        self.batch_norm = batch_norm
        self.acti_func = acti_func
        self.groups = groups
        if not dim == 2:
            if not dim == 3:
                raise AssertionError
        if dim == 2:
            self.conv1x1 = nn.Conv2d(in_channels, out_channels, kernel_size=1,
              stride=1,
              padding=0,
              dilation=dilation,
              groups=(self.groups),
              bias=bias)
            self.conv = nn.ConvTranspose2d(out_channels, out_channels, kernel_size,
              stride, padding, output_padding, groups=out_channels,
              bias=bias,
              dilation=dilation)
            if self.batch_norm:
                self.bn = nn.BatchNorm2d(out_channels)
        else:
            self.conv1x1 = nn.Conv3d(in_channels, out_channels, kernel_size=1,
              stride=1,
              padding=0,
              dilation=dilation,
              groups=(self.groups),
              bias=bias)
            self.conv = nn.ConvTranspose3d(out_channels, out_channels, kernel_size,
              stride, padding, output_padding, groups=out_channels,
              bias=bias,
              dilation=dilation)
        if self.batch_norm:
            self.bn = nn.BatchNorm3d(out_channels)

    def forward(self, x):
        f = self.conv1x1(x)
        f = self.conv(f)
        if self.batch_norm:
            f = self.bn(f)
        if self.acti_func is not None:
            f = self.acti_func(f)
        return f
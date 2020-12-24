# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/b3ql/.virtualenvs/SSD/lib/python3.7/site-packages/ssd/layers/separable_conv.py
# Compiled at: 2019-10-28 14:34:58
# Size of source mod 2**32: 674 bytes
from torch import nn

class SeparableConv2d(nn.Module):

    def __init__(self, in_channels, out_channels, kernel_size=1, stride=1, padding=0, onnx_compatible=False):
        super().__init__()
        ReLU = nn.ReLU if onnx_compatible else nn.ReLU6
        self.conv = nn.Sequential(nn.Conv2d(in_channels=in_channels, out_channels=in_channels, kernel_size=kernel_size, groups=in_channels,
          stride=stride,
          padding=padding), nn.BatchNorm2d(in_channels), ReLU(), nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=1))

    def forward(self, x):
        return self.conv(x)
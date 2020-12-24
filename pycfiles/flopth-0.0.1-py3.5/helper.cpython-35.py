# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/flopth/helper.py
# Compiled at: 2019-02-21 08:32:45
# Size of source mod 2**32: 3065 bytes
""" Useful tools. Stolen from here: https://github.com/Swall0w/torchstat"""
import numpy as np, torch, torch.nn as nn

def compute_flops(module, inp, out):
    if isinstance(module, nn.Conv2d):
        return compute_Conv2d_flops(module, inp, out)
    else:
        if isinstance(module, nn.BatchNorm2d):
            return compute_BatchNorm2d_flops(module, inp, out)
        if isinstance(module, (nn.AvgPool2d, nn.MaxPool2d)):
            return compute_Pool2d_flops(module, inp, out)
        if isinstance(module, (nn.ReLU, nn.ReLU6, nn.PReLU, nn.ELU, nn.LeakyReLU)):
            return compute_ReLU_flops(module, inp, out)
        if isinstance(module, nn.Upsample):
            return compute_Upsample_flops(module, inp, out)
        if isinstance(module, nn.Linear):
            return compute_Linear_flops(module, inp, out)
        return 0


def compute_Conv2d_flops(module, inp, out):
    assert isinstance(module, nn.Conv2d)
    assert len(inp.size()) == 4 and len(inp.size()) == len(out.size())
    batch_size = inp.size()[0]
    in_c = inp.size()[1]
    k_h, k_w = module.kernel_size
    out_c, out_h, out_w = out.size()[1:]
    groups = module.groups
    filters_per_channel = out_c // groups
    conv_per_position_flops = k_h * k_w * in_c * filters_per_channel
    active_elements_count = batch_size * out_h * out_w
    total_conv_flops = conv_per_position_flops * active_elements_count
    bias_flops = 0
    if module.bias is not None:
        bias_flops = out_c * active_elements_count
    total_flops = total_conv_flops + bias_flops
    return total_flops


def compute_BatchNorm2d_flops(module, inp, out):
    assert isinstance(module, nn.BatchNorm2d)
    assert len(inp.size()) == 4 and len(inp.size()) == len(out.size())
    in_c, in_h, in_w = inp.size()[1:]
    batch_flops = np.prod(inp.shape)
    if module.affine:
        batch_flops *= 2
    return batch_flops


def compute_ReLU_flops(module, inp, out):
    assert isinstance(module, (nn.ReLU, nn.ReLU6, nn.PReLU, nn.ELU, nn.LeakyReLU))
    batch_size = inp.size()[0]
    active_elements_count = batch_size
    for s in inp.size()[1:]:
        active_elements_count *= s

    return active_elements_count


def compute_Pool2d_flops(module, inp, out):
    if not isinstance(module, nn.MaxPool2d):
        assert isinstance(module, nn.AvgPool2d)
        assert len(inp.size()) == 4 and len(inp.size()) == len(out.size())
        return np.prod(inp.shape)


def compute_Linear_flops(module, inp, out):
    assert isinstance(module, nn.Linear)
    assert len(inp.size()) == 2 and len(out.size()) == 2
    batch_size = inp.size()[0]
    return batch_size * inp.size()[1] * out.size()[1]


def compute_Upsample_flops(module, inp, out):
    assert isinstance(module, nn.Upsample)
    output_size = out[0]
    batch_size = inp.size()[0]
    output_elements_count = batch_size
    for s in output_size.shape[1:]:
        output_elements_count *= s

    return output_elements_count
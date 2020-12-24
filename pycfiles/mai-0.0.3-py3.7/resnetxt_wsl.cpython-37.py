# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mai\models\resnetxt_wsl.py
# Compiled at: 2020-03-12 03:34:07
# Size of source mod 2**32: 4081 bytes
"""
    Code From : https://github.com/facebookresearch/WSL-Images/blob/master/hubconf.py
"""
__all__ = [
 'resnext101_32x8d_wsl', 'resnext101_32x16d_wsl', 'resnext101_32x32d_wsl', 'resnext101_32x48d_wsl']
dependencies = [
 'torch', 'torchvision']
try:
    from torch.hub import load_state_dict_from_url
except ImportError:
    import torch.utils.model_zoo as load_state_dict_from_url

from .resnet import ResNet, Bottleneck
model_urls = {'resnext101_32x8d':'https://download.pytorch.org/models/ig_resnext101_32x8-c38310e5.pth', 
 'resnext101_32x16d':'https://download.pytorch.org/models/ig_resnext101_32x16-c6f796b0.pth', 
 'resnext101_32x32d':'https://download.pytorch.org/models/ig_resnext101_32x32-e4b90b00.pth', 
 'resnext101_32x48d':'https://download.pytorch.org/models/ig_resnext101_32x48-3e41cc8a.pth'}

def _resnext(arch, block, layers, pretrained, progress, **kwargs):
    model = ResNet(block, layers, **kwargs)
    state_dict = load_state_dict_from_url((model_urls[arch]), progress=progress)
    new_state_dict = model.state_dict()
    new_state_dict.update(state_dict)
    model.load_state_dict(new_state_dict)
    return model


def resnext101_32x8d_wsl(pretrained=False, progress=True, **kwargs):
    """Constructs a ResNeXt-101 32x8 model pre-trained on weakly-supervised data
    and finetuned on ImageNet from Figure 5 in
    `"Exploring the Limits of Weakly Supervised Pretraining" <https://arxiv.org/abs/1805.00932>`_
    Args:
        progress (bool): If True, displays a progress bar of the download to stderr.
    """
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 8
    return _resnext('resnext101_32x8d', Bottleneck, [3, 4, 23, 3], pretrained, progress, **kwargs)


def resnext101_32x16d_wsl(pretrained=False, progress=True, **kwargs):
    """Constructs a ResNeXt-101 32x16 model pre-trained on weakly-supervised data
    and finetuned on ImageNet from Figure 5 in
    `"Exploring the Limits of Weakly Supervised Pretraining" <https://arxiv.org/abs/1805.00932>`_
    Args:zz
        progress (bool): If True, displays a progress bar of the download to stderr.
    """
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 16
    return _resnext('resnext101_32x16d', Bottleneck, [3, 4, 23, 3], pretrained, progress, **kwargs)


def resnext101_32x32d_wsl(pretrained=False, progress=True, **kwargs):
    """Constructs a ResNeXt-101 32x32 model pre-trained on weakly-supervised data
    and finetuned on ImageNet from Figure 5 in
    `"Exploring the Limits of Weakly Supervised Pretraining" <https://arxiv.org/abs/1805.00932>`_
    Args:
        progress (bool): If True, displays a progress bar of the download to stderr.
    """
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 32
    return _resnext('resnext101_32x32d', Bottleneck, [3, 4, 23, 3], pretrained, progress, **kwargs)


def resnext101_32x48d_wsl(pretrained=False, progress=True, **kwargs):
    """Constructs a ResNeXt-101 32x48 model pre-trained on weakly-supervised data
    and finetuned on ImageNet from Figure 5 in
    `"Exploring the Limits of Weakly Supervised Pretraining" <https://arxiv.org/abs/1805.00932>`_
    Args:
        progress (bool): If True, displays a progress bar of the download to stderr.
    """
    kwargs['groups'] = 32
    kwargs['width_per_group'] = 48
    return _resnext('resnext101_32x48d', Bottleneck, [3, 4, 23, 3], pretrained, progress, **kwargs)
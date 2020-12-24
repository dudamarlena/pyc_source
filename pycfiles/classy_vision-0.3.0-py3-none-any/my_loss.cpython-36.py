# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/aadcock/projects/ClassyVision-2/classy_vision/templates/synthetic/losses/my_loss.py
# Compiled at: 2020-03-04 13:49:51
# Size of source mod 2**32: 617 bytes
import torch.nn.functional as F
from classy_vision.losses import ClassyLoss, register_loss

@register_loss('my_loss')
class MyLoss(ClassyLoss):

    def forward(self, input, target):
        labels = F.one_hot(target, num_classes=2).float()
        return F.binary_cross_entropy(input, labels)

    @classmethod
    def from_config(cls, config):
        return cls()
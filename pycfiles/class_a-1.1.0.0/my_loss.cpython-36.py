# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mannatsingh/dev/git/upstream/ClassyVision/classy_vision/templates/synthetic/losses/my_loss.py
# Compiled at: 2020-04-29 11:26:04
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
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/mannatsingh/dev/git/upstream/ClassyVision/classy_vision/templates/synthetic/models/my_model.py
# Compiled at: 2020-04-29 11:26:04
# Size of source mod 2**32: 754 bytes
import torch.nn as nn, torchvision.models as models
from classy_vision.models import ClassyModel, register_model

@register_model('my_model')
class MyModel(ClassyModel):

    def __init__(self):
        super().__init__()
        self.model = nn.Sequential(nn.AdaptiveAvgPool2d((20, 20)), nn.Flatten(1), nn.Linear(1200, 2), nn.Sigmoid())

    def forward(self, x):
        x = self.model(x)
        return x

    @classmethod
    def from_config(cls, config):
        return cls()
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zeus/PyTorch-Hackathon-2019/rectifai/models/posturenet/network.py
# Compiled at: 2019-09-17 12:17:44
# Size of source mod 2**32: 664 bytes
import torch
import torch.nn as nn
import torch.nn.functional as F
from .config import *

class PostureNetwork(nn.Module):

    def __init__(self, input_size=input_size, hidden_sizes=hidden_sizes, n_classes=n_classes):
        super(PostureNetwork, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_sizes[0])
        self.fc2 = nn.Linear(hidden_sizes[0], hidden_sizes[1])
        self.fc3 = nn.Linear(hidden_sizes[1], n_classes)
        self.relu = nn.ReLU()

    def forward(self, x):
        out = self.fc1(x)
        out = self.relu(out)
        out = self.fc2(out)
        out = self.relu(out)
        out = self.fc3(out)
        return out
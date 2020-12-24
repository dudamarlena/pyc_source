# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mai\losses\contrastive.py
# Compiled at: 2020-03-10 04:24:35
# Size of source mod 2**32: 570 bytes
import torch
import torch.nn.functional as F

class ContrastiveLoss(torch.nn.Module):

    def __init__(self, margin=2.0):
        super(ContrastiveLoss, self).__init__()
        self.margin = margin

    def forward(self, output1, output2, label):
        euclidean_distance = F.pairwise_distance(output1, output2)
        loss_contrastive = torch.mean(label * torch.pow(euclidean_distance, 2) + (1 - label) * torch.pow(torch.clamp((self.margin - euclidean_distance), min=0.0), 2))
        return loss_contrastive * 0.5
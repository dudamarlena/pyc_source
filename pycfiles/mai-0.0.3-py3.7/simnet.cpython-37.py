# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\mai\models\twin\simnet.py
# Compiled at: 2020-03-10 05:19:54
# Size of source mod 2**32: 1980 bytes
import torch.nn as nn

class SiameseNetwork(nn.Module):
    __doc__ = '\n      最简单的孪生网络\n      输入形状：\n            1，100，100\n      输入：\n            num_classes(int) 模型测试的类的数目\n      例程：\n            model = sai.models.twin.SiameseNetwork()\n            criterion  = sai.losses.ContrastiveLoss()\n            out1, out2 = model(torch.rand(1,1,100,100), torch.rand(1,1,100,100))\n            loss = criterion(out1, out2, 1)\n      '

    def __init__(self, num_classes=2):
        super(SiameseNetwork, self).__init__()
        self.cnn1 = nn.Sequential(nn.ReflectionPad2d(1), nn.Conv2d(1, 4, kernel_size=3), nn.ReLU(inplace=True), nn.BatchNorm2d(4), nn.Dropout2d(p=0.2), nn.ReflectionPad2d(1), nn.Conv2d(4, 8, kernel_size=3), nn.ReLU(inplace=True), nn.BatchNorm2d(8), nn.Dropout2d(p=0.2), nn.ReflectionPad2d(1), nn.Conv2d(8, 8, kernel_size=3), nn.ReLU(inplace=True), nn.BatchNorm2d(8), nn.Dropout2d(p=0.2))
        self.fc1 = nn.Sequential(nn.Linear(80000, 500), nn.ReLU(inplace=True), nn.Linear(500, 500), nn.ReLU(inplace=True), nn.Linear(500, num_classes))

    def forward_once(self, x):
        output = self.cnn1(x)
        output = output.view(output.size()[0], -1)
        output = self.fc1(output)
        return output

    def forward(self, input1, input2):
        output1 = self.forward_once(input1)
        output2 = self.forward_once(input2)
        return (output1, output2)
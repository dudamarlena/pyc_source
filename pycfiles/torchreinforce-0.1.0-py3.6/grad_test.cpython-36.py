# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/torchreinforce/tests/grad_test.py
# Compiled at: 2019-01-18 10:35:00
# Size of source mod 2**32: 906 bytes
from unittest import TestCase
import torch
from torchreinforce import ReinforceModule

class TestModel(ReinforceModule):

    def __init__(self):
        super(TestModel, self).__init__()
        self.net = torch.nn.Sequential(torch.nn.Linear(2, 2), torch.nn.Sigmoid())

    @ReinforceModule.forward
    def forward(self, x):
        return self.net(x)


class TestGrad(TestCase):

    def test_grad(self):
        device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
        net = TestModel().to(device)
        o1 = net(torch.randn(2).to(device))
        o2 = net(torch.randn(2).to(device))
        o3 = net(torch.randn(2).to(device))
        if not type(o1.get()) == int:
            raise AssertionError
        else:
            assert type(o2.get()) == int
            o1.reward(1)
            o2.reward(2)
            loss = net.loss()
            assert loss.grad_fn is not None
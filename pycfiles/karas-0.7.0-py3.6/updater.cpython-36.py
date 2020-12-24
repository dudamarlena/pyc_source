# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test/updater.py
# Compiled at: 2019-01-07 10:21:40
# Size of source mod 2**32: 891 bytes
import torch.nn as nn, karas.training.updater as updater

class Updater(updater.Updater):

    def __init__(self, model, **kwargs):
        (super(Updater, self).__init__)(**kwargs)
        self.model = model
        self.criterion = nn.NLLLoss().to(self.device)

    def converter(self, batch):
        input, target = batch
        input, target = input.to(self.device), target.to(self.device)
        return (input, target)

    def update(self, batch):
        input, target = self.converter(batch)
        output = self.model(input)
        loss = self.criterion(output, target)
        self.optimizers['net'].zero_grad()
        loss.backward()
        self.optimizers['net'].step()
        with self.reporter.scope('scalar'):
            self.reporter.report({'loss': loss.item()})
        with self.reporter.scope('images'):
            self.reporter.report({'input': input})
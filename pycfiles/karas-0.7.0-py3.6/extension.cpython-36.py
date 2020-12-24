# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test/extension.py
# Compiled at: 2019-01-08 04:36:11
# Size of source mod 2**32: 903 bytes
import torch
from karas.training import extension

class Eval(extension.Extension):

    def initialize(self, trainer):
        pass

    def __call__(self, trainer):
        updater = trainer.updater
        reporter = trainer.reporter
        loader = trainer.get_loader('test')
        correct = 0
        updater.model.eval()
        torch.set_grad_enabled(False)
        for batch in loader:
            input, target = updater.converter(batch)
            output = updater.model(input)
            pred = output.max(1, keepdim=True)[1]
            correct += pred.eq(target.view_as(pred)).sum().item()

        accuracy = correct / len(loader.dataset)
        with reporter.scope('scalar'):
            reporter.report({'accuracy': accuracy})
        updater.model.train()
        torch.set_grad_enabled(True)

    def finalize(self):
        pass
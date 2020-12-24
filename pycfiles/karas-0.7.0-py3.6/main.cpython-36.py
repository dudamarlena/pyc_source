# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/test/main.py
# Compiled at: 2019-01-08 02:00:31
# Size of source mod 2**32: 2797 bytes
import torch, pickle
from torch.optim import SGD, lr_scheduler
from torchvision.datasets import MNIST
from torch.utils.data import DataLoader
from torchvision.transforms import transforms
import karas
from karas.training.extension import *
from karas.training.extensions import LogReport
from karas.training.extensions import LrObserver
from karas.training.extensions import LrScheduler
from karas.training.extensions import PrintReport
from karas.training.extensions import Snapshot
from karas.training.extensions import ProgressBar
from karas.training.extensions import TensorBoard
from karas.training.trainer import Trainer
from karas.training.triggers import EarlyStoppingTrigger
from karas.training.triggers import MaxValueTrigger
from extension import Eval
from net import Net
from updater import Updater
resume = False
loaders = {}
loaders['train'] = DataLoader(MNIST('../data', train=True, download=True, transform=(transforms.Compose([
 transforms.ToTensor()]))),
  batch_size=16)
loaders['test'] = DataLoader(MNIST('../data', train=False, download=True, transform=(transforms.Compose([
 transforms.ToTensor()]))))
keys = [
 'epoch', 'iteration', 'test/accuracy', 'loss', 'net/lr', 'elapsed_time']
device = torch.device('cpu')
net = Net().to(device)
opt = SGD((net.parameters()), lr=0.01, momentum=0.5)
stopper = EarlyStoppingTrigger(monitor='test/accuracy', patients=3, max_trigger=(10,
                                                                                 'epoch'))
updater = Updater(model=net, optimizers={'net': opt}, device=device)
trainer = Trainer(updater, stop_trigger=stopper, loaders=loaders)
trainer.extend(Snapshot(filename='snapshot_iter_{.iteration}.pkl'), priority=PRIORITY_READER, trigger=(1,
                                                                                                       'epoch'))
trainer.extend((Snapshot(net, 'net_{.iteration}.pth')), priority=PRIORITY_READER, trigger=MaxValueTrigger(key='accuracy'))
trainer.extend((Eval()), priority=PRIORITY_WRITER, trigger=(1, 'epoch'))
trainer.extend((LogReport(keys)), trigger=(100, 'iteration'))
trainer.extend((TensorBoard()), trigger=(10, 'iteration'))
trainer.extend((PrintReport(keys)), trigger=(100, 'iteration'))
trainer.extend((LrObserver()), trigger=(100, 'iteration'))
trainer.extend((LrScheduler(lr_scheduler.StepLR(opt, step_size=2, gamma=0.5))), trigger=(1,
                                                                                         'epoch'))
trainer.extend(ProgressBar(update_interval=1))
if resume:
    trainer = karas.deserialize('output/snapshot_iter_1000.pkl')
trainer.run()
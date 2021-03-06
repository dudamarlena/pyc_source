# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/anaconda3/lib/python3.6/site-packages/vnlp/model/model.py
# Compiled at: 2018-06-22 04:07:56
# Size of source mod 2**32: 4391 bytes
import torch, os, re, logging, pprint, json, numpy as np
from argparse import Namespace
from torch import nn
from torch.nn import functional as F
from collections import defaultdict
from importlib import import_module
from ..utils.logging import get_logger
from ..exp.tracker import Tracker
from ..exp.grapher import Grapher

class Model:
    __doc__ = '\n    args has:\n    - gpu\n    - dexp\n    - module\n    - name\n    - epoch\n    - early_stop\n    '

    def __init__(self, args, module):
        self.args = args
        self.device = torch.device('cuda') if args.gpu else torch.device('cpu')
        self.module = module

    def to(self, device):
        if isinstance(list):
            self.module = nn.DataParallel((self.module), device_ids=device)
        else:
            self.module = self.module.to(torch.device(device))

    @property
    def module_instance(self):
        if isinstance(self.module, nn.DataParallel):
            return self.module.module
        else:
            return self.module

    @property
    def dout(self):
        return os.path.join(self.args.dexp, self.args.module, self.args.name)

    @classmethod
    def from_module(cls, name, args, *vargs, module_root='modules', **kwargs):
        M = import_module('{}.{}'.format(module_root, name)).Model
        return cls(args, M(args, *vargs, **kwargs))

    def run_train(self, train, dev, optimizer=None, tracker=None, logging_level=logging.INFO, verbose=True):
        if optimizer is None:
            optimizer = torch.optim.Adam(self.module.parameters())
        if not os.path.isdir(self.dout):
            os.makedirs(self.dout)
        logger = get_logger('trainer', fout=(os.path.join(self.dout, 'train.log')), level=logging_level)
        tracker = tracker or Tracker()
        grapher = Grapher(self.dout)
        tracker.save_data(vars(self.args), 'config.json')
        iteration = tracker.iteration
        for epoch in range(tracker.epoch, self.args.epoch):
            logger.info('Starting epoch {}'.format(epoch))
            loss = 0
            self.module.train()
            for batch in train.batch((self.args.batch), shuffle=True, verbose=verbose):
                optimizer.zero_grad()
                feat = self.module_instance.featurize(batch, device=(self.device))
                if not grapher.plotted_module:
                    grapher.plot_module(self.module_instance, feat)
                out = self.module(feat)
                batch_loss = self.module_instance.compute_loss(out, batch)
                batch_loss.backward()
                optimizer.step()
                loss += batch_loss.item()
                iteration += len(batch)

            train_preds = self.run_pred(train)
            dev_preds = self.run_pred(dev)
            train_metrics = train.compute_metrics(train_preds)
            train_metrics['loss'] = loss
            metrics = {'iteration':iteration, 
             'epoch':epoch, 
             'train':train_metrics, 
             'dev':dev.compute_metrics(dev_preds)}
            self.module_instance.graph(grapher, metrics, iteration)
            if tracker.is_best(metrics, (self.args.early_stop), iteration=iteration, epoch=epoch):
                logging.info('Found new best! Saving to {}'.format(self.dout))
                tracker.save_checkpoint((self.dout), metrics, (self.args.early_stop), (self.module_instance), optimizer, (self.args), link_best=True)
                tracker.clean_old_checkpoints(self.dout, self.args.early_stop)
                tracker.save_data(train_preds, os.path.join(self.dout, 'train.preds.json'))
                tracker.save_data(dev_preds, os.path.join(self.dout, 'dev.preds.json'))
                metrics['best'] = metrics['dev']
            logger.info('\n' + pprint.pformat(metrics))
            tracker.save(os.path.join(self.dout, 'tracker.json'))

        state = tracker.load_best_checkpoint(self.dout, self.args.early_stop)
        self.module_instance.load_state_dict(state['module'])
        optimizer.load_state_dict(state['optimizer'])

    def run_pred(self, dev, verbose=False):
        self.module.eval()
        preds = []
        for batch in dev.batch((self.args.batch), shuffle=False, verbose=verbose):
            out = self.module(self.module_instance.featurize(batch))
            preds += self.module_instance.extract_preds(out, batch)

        return preds
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/deeplearn/module.py
# Compiled at: 2020-05-11 01:33:34
# Size of source mod 2**32: 1433 bytes
"""Base PyTorch module and utilities.

"""
__author__ = 'Paul Landes'
from abc import abstractmethod, ABCMeta
import logging, torch
from torch import nn
from zensols.deeplearn import Batch, NetworkSettings, EarlyBailException
logger = logging.getLogger(__name__)

class BaseNetworkModule(nn.Module, metaclass=ABCMeta):
    __doc__ = 'A recurrent neural network model that is used to classify sentiment.\n\n    '

    def __init__(self, net_settings, sub_logger=None):
        super().__init__()
        self.net_settings = net_settings
        if sub_logger is None:
            self.logger = logger
        else:
            self.logger = sub_logger

    @abstractmethod
    def _forward(self, batch: Batch) -> torch.Tensor:
        """The model's forward implementation.  Normal backward semantics are no
        different.

        :param batch: the batch to train, validate or test on

        """
        pass

    @property
    def device(self):
        """Return the device on which the model is configured.

        """
        return next(self.parameters()).device

    def forward(self, batch: Batch):
        x = self._forward(batch)
        if self.net_settings.debug:
            raise EarlyBailException()
        return x

    def _shape_debug(self, msg, x):
        if self.net_settings.debug:
            self.logger.debug(f"{msg}: x: {x.shape}")
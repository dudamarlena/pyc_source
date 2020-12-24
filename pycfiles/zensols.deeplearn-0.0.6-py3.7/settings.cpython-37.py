# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/zensols/deeplearn/settings.py
# Compiled at: 2020-05-11 01:33:34
# Size of source mod 2**32: 3150 bytes
"""This file contains classes that configure the network and classifier runs.

"""
__author__ = 'Paul Landes'
from dataclasses import dataclass, field
from abc import ABC, abstractmethod
import sys, logging
from pathlib import Path
import torch.nn.functional as F
from zensols.deeplearn import TorchConfig
logger = logging.getLogger(__name__)

class EarlyBailException(Exception):
    __doc__ = 'Convenience used for helping debug the network.\n\n    '

    def __init__(self):
        super().__init__('early bail to debug the network')


@dataclass
class NetworkSettings(ABC):
    __doc__ = 'A container settings class for network models.  This abstract class must\n    return the fully qualified (with module name) PyTorch `model\n    (`torch.nn.Module``) that goes along with these settings.  An instance of\n    this class is saved in the model file and given back to it when later\n    restored.\n\n    :torch_config: the configuration used to copy memory (i.e. GPU) of the\n                   model\n\n    :param dropout: if not ``None``, add a dropout on the fully connected\n                    layer\n\n    :param activation: if ``True`` use a rectified linear activation function\n\n    :param debug: if ``True``, raise an error on the first forward pass\n\n\n    :see ModelSettings:\n\n    '
    torch_config: TorchConfig
    dropout: float
    activation: str
    debug: bool

    @abstractmethod
    def get_module_class_name(self) -> str:
        pass

    @property
    def activation_function(self):
        if self.activation == 'relu':
            activation = F.relu
        else:
            if self.activation == 'softmax':
                activation = F.softmax
            else:
                activation = None
        return activation

    def __str__(self):
        return f"{super().__str__()},  activation={self.activation}"


@dataclass
class ModelSettings(object):
    __doc__ = 'This configures and instance of ``ModelManager``.  This differes from\n    ``NetworkSettings`` in that it configures the model parameters, and not the\n    neural network parameters.\n\n    Another reason for these two separate classes is data in this class is not\n    needed to rehydrate an instance of ``torch.nn..Module``.\n\n    :param path: the path to save and load the model\n    :\n    :param learning_rate: learning_rate used for the gradient descent step\n                          (done in the optimzer)\n    :param epochs: the number of epochs to train the network\n\n    :param batch_iteration: how the batches are buffered; one of ``gpu``, which\n                            buffers all data in the GPU, ``cpu``, which means\n                            keep all batches in CPU memory (the default), or\n                            ``buffered`` which means to buffer only one batch\n                            at a time (only for *very* large data)\n\n    :param use_gc: if ``True``, invoke the garbage collector periodically to\n                   reduce memory overhead\n\n    :see NetworkSettings:\n\n    '
    path: Path
    learning_rate: float
    epochs: int
    batch_limit = field(default=(sys.maxsize))
    batch_limit: int
    batch_iteration = field(default='cpu')
    batch_iteration: str
    use_gc = field(default=False)
    use_gc: bool
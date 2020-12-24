# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/allrank/models/model_utils.py
# Compiled at: 2020-02-21 08:15:29
# Size of source mod 2**32: 1574 bytes
import torch, numpy as np
import torch.nn as nn
from allrank.utils.ltr_logging import get_logger
logger = get_logger()

def get_torch_device():
    """
    Getter for an available pyTorch device.
    :return: CUDA-capable GPU if available, CPU otherwise
    """
    if torch.cuda.is_available():
        return torch.device('cuda:0')
    return torch.device('cpu')


def get_num_params(model: nn.Module) -> int:
    """
    Calculation of the number of nn.Module parameters.
    :param model: nn.Module
    :return: number of parameters
    """
    model_parameters = filter(lambda p: p.requires_grad, model.parameters())
    params = sum([np.prod(p.size()) for p in model_parameters])
    return params


def log_num_params(num_params: int) -> None:
    """
    Logging num_params to the global logger.
    :param num_params: number of parameters to log
    """
    logger.info('Model has {} trainable parameters'.format(num_params))


class CustomDataParallel(nn.DataParallel):
    __doc__ = '\n    Wrapper for scoring with nn.DataParallel object containing LTRModel.\n    '

    def score(self, x, mask, indices):
        """
        Wrapper function for a forward pass through the whole LTRModel and item scoring.
        :param x: input of shape [batch_size, slate_length, input_dim]
        :param mask: padding mask of shape [batch_size, slate_length]
        :param indices: original item ranks used in positional encoding, shape [batch_size, slate_length]
        :return: scores of shape [batch_size, slate_length]
        """
        return self.module.score(x, mask, indices)
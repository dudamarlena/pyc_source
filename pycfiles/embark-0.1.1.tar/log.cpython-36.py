# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/naresh/Projects/embark/embark/tensorflow_classifier/utils/log.py
# Compiled at: 2020-01-31 20:51:35
# Size of source mod 2**32: 2057 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, datetime, numpy as np

def get_valid_time_stamp():
    """ Get a valid time stamp without illegal characters.
    Adds time_ to make the time stamp a valid table name in sql.
    Returns (string): extracted timestamp
    """
    time_stamp = str(datetime.datetime.now())
    time_stamp = time_stamp.replace('-', '_').replace(':', '_').replace(' ', '_').replace('.', '_')
    return time_stamp


def form_results_folder(results_path, model_name):
    """ Forms folders for each run to store the tensorboard files, saved models and the log files.
    Args:
        results_path (str): results directory
        model_name (str): model name
    Returns: three string pointing to tensorboard, saved models and log paths respectively.
    """
    folder_name = '{}_{}'.format(model_name, get_valid_time_stamp())
    tensorboard_path = os.path.join(results_path, folder_name + '/Tensorboard')
    saved_model_path = os.path.join(results_path, folder_name + '/Saved_models')
    log_path = os.path.join(results_path, folder_name + '/log')
    if not os.path.exists(os.path.join(results_path + folder_name)):
        os.makedirs(os.path.join(results_path, folder_name))
        os.makedirs(tensorboard_path)
        os.makedirs(saved_model_path)
        os.makedirs(log_path)
    return (
     tensorboard_path, saved_model_path, log_path)


class AverageMeter(object):
    __doc__ = ' Computes and stores the average and current value.\n    '

    def __init__(self):
        self.data = []
        self.reset()
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def reset(self):
        self.val = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, val, n=1):
        self.data.append(val)
        self.val = val
        self.sum += val * n
        self.count += n
        self.avg = self.sum / self.count

    def median(self):
        return np.median(self.data)
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/yarlp/utils/experiment_utils.py
# Compiled at: 2018-03-04 11:41:49
# Size of source mod 2**32: 1121 bytes
import os, json, inspect, importlib
from datetime import datetime
from functools import partial

def _get_agent_cls_dict():
    import yarlp.agent
    clsmembers = inspect.getmembers(yarlp.agent, inspect.isclass)
    return dict(clsmembers)


def _get_datetime_str():
    return datetime.now().strftime('_%Y-%m-%d_%H-%M-%S')


def _create_log_directory(name, prepend_dir_name):
    name += _get_datetime_str()
    full_dir = os.path.join(prepend_dir_name, name)
    if not os.path.exists(full_dir):
        os.makedirs(full_dir)
    return full_dir


def _save_spec_to_dir(spec, dir):
    file_path = os.path.join(dir, 'spec.json')
    json.dump(spec, open(file_path, 'w'), indent=4)


def _get_model_from_str(x):
    """
    Loads a model from a string
    Parameters
    --------------
    x : str, must exist in yarlp.models
    """
    m = importlib.import_module('yarlp.model')
    return getattr(m, x)


def get_network(network, params):
    if isinstance(network, str):
        network = _get_model_from_str(network)
    network = partial(network, **params)
    return network
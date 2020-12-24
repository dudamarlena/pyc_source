# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/projects_nils/photon_core/photonai/optimization/config_grid.py
# Compiled at: 2019-11-21 09:20:09
# Size of source mod 2**32: 2992 bytes
from photonai.optimization import PhotonHyperparam, IntegerRange, FloatRange, Categorical, BooleanSwitch
from photonai.photonlogger import logger
from itertools import product
import numpy as np

def create_global_config_dict(pipeline_elements):
    global_hyperparameter_dict = {}
    for p_element in pipeline_elements:
        if len(p_element.hyperparameters) > 0:
            for h_key, h_value in p_element.hyperparameters.items():
                if isinstance(h_value, list):
                    global_hyperparameter_dict[h_key] = h_value
                elif isinstance(h_value, PhotonHyperparam):
                    if isinstance(h_value, FloatRange) or isinstance(h_value, IntegerRange):
                        h_value.transform()
                        global_hyperparameter_dict[h_key] = h_value.values
                if isinstance(h_value, BooleanSwitch) or isinstance(h_value, Categorical):
                    global_hyperparameter_dict[h_key] = h_value.values

    return global_hyperparameter_dict


def create_global_config_grid(pipeline_elements, add_name=''):
    global_hyperparameter_list = []
    for element in pipeline_elements:
        if hasattr(element, 'generate_config_grid'):
            config_grid = element.generate_config_grid()
            if len(config_grid) > 0:
                global_hyperparameter_list.append(config_grid)

    praefix = ''
    if add_name != '':
        praefix = add_name + '__'
    threshold = 1000000
    total_product_num = 1
    for i in global_hyperparameter_list:
        total_product_num = total_product_num * len(i)

    if total_product_num > threshold:
        warn_text = 'The entire configuration grid entails more than ' + str(threshold) + ' possible configurations. This might take veeeeeeery looooong to both compute and process.'
        logger.warn(warn_text)
        raise Warning(warn_text)
    config_list = list(product(*global_hyperparameter_list))
    config_dicts = []
    for c in config_list:
        config_dicts.append(dict(((praefix + pair[0], pair[1]) for d in c for pair in d.items())))

    return config_dicts
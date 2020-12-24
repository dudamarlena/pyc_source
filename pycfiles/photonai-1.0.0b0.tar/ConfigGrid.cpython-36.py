# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nwinter/PycharmProjects/photon_projects/photon_core/photonai/optimization/ConfigGrid.py
# Compiled at: 2019-02-21 07:32:17
# Size of source mod 2**32: 2212 bytes
from .Hyperparameters import PhotonHyperparam, FloatRange, IntegerRange, BooleanSwitch, Categorical
from itertools import product

def create_global_config_dict(pipeline_elements):
    global_hyperparameter_dict = {}
    for p_element in pipeline_elements:
        if len(p_element.hyperparameters) > 0:
            for h_key, h_value in p_element.hyperparameters.items():
                if isinstance(h_value, list):
                    global_hyperparameter_dict[h_key] = h_value
                else:
                    if isinstance(h_value, PhotonHyperparam):
                        if isinstance(h_value, FloatRange) or isinstance(h_value, IntegerRange):
                            h_value.transform()
                            global_hyperparameter_dict[h_key] = h_value.values
                        elif isinstance(h_value, BooleanSwitch) or isinstance(h_value, Categorical):
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
    config_list = list(product(*global_hyperparameter_list))
    config_dicts = []
    for c in config_list:
        config_dicts.append(dict((praefix + pair[0], pair[1]) for d in c for pair in d.items()))

    return config_dicts
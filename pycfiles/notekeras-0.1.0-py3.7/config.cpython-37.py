# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/notekeras/model/retinanet/utils/config.py
# Compiled at: 2020-04-22 04:57:48
# Size of source mod 2**32: 1167 bytes
import configparser, numpy as np
import tensorflow.keras.backend as K
from notekeras.model.retinanet.utils.anchors import AnchorParameters

def read_config_file(config_path):
    config = configparser.ConfigParser()
    with open(config_path, 'r') as (file):
        config.read_file(file)
    assert 'anchor_parameters' in config, 'Malformed config file. Verify that it contains the anchor_parameters section.'
    config_keys = set(config['anchor_parameters'])
    default_keys = set(AnchorParameters.default.__dict__.keys())
    assert config_keys <= default_keys, 'Malformed config file. These keys are not valid: {}'.format(config_keys - default_keys)
    return config


def parse_anchor_parameters(config):
    ratios = np.array(list(map(float, config['anchor_parameters']['ratios'].split(' '))), K.floatx())
    scales = np.array(list(map(float, config['anchor_parameters']['scales'].split(' '))), K.floatx())
    sizes = list(map(int, config['anchor_parameters']['sizes'].split(' ')))
    strides = list(map(int, config['anchor_parameters']['strides'].split(' ')))
    return AnchorParameters(sizes, strides, ratios, scales)
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/evaluator/evaluator_config.py
# Compiled at: 2018-12-10 18:39:29
import os
from ..utils import parse_configs
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_config.yaml')

def get_config(paths=None, config=None):
    if paths is None:
        paths = []
    paths = [
     DEFAULT_CONFIG_PATH] + paths
    configuration = parse_configs(paths)
    if config is not None:
        configuration.update(config)
    return configuration
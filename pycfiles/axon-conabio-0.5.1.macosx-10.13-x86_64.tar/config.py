# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/management/config.py
# Compiled at: 2018-12-10 18:39:29
import os
from ..utils import memoized, parse_configs
DEFAULT_CONFIG_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'default_config.yaml')

@memoized
def get_config(path=None, config=None):
    if path is None:
        path = []
    else:
        path = [
         path]
    paths = [DEFAULT_CONFIG_PATH] + path
    configuration = parse_configs(paths)
    if config is not None:
        configuration.update(config)
    return configuration


def get_project_config(project):
    project_config = os.path.join(project, '.project', 'axon_config.yaml')
    return get_config(path=project_config)
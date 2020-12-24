# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/axon_conabio/management/make_project.py
# Compiled at: 2018-12-10 18:39:29
import os, shutil
from .utils import get_base_project
CURRENT_DIR = os.path.abspath(os.path.dirname(__file__))
TYPES = [
 'models_dir',
 'losses_dir',
 'metrics_dir',
 'architectures_dir',
 'datasets_dir',
 'products_dir',
 'preprocessors_dir']

def make_project(path, config):
    project = get_base_project(path)
    if project is not None:
        msg = 'Cannot create a new project within another project'
        msg += ' directory!'
        raise ValueError(msg)
    os.makedirs(path)
    struct_conf = config['structure']
    for type_ in TYPES:
        dirname = struct_conf[type_]
        os.makedirs(os.path.join(path, dirname))

    os.makedirs(os.path.join(path, '.project'))
    shutil.copy(os.path.join(CURRENT_DIR, 'default_config.yaml'), os.path.join(path, '.project', 'axon_config.yaml'))
    shutil.copy(os.path.join(CURRENT_DIR, '../trainer/default_config.yaml'), os.path.join(path, '.project', 'train.yaml'))
    shutil.copy(os.path.join(CURRENT_DIR, '../evaluator/default_config.yaml'), os.path.join(path, '.project', 'evaluation.yaml'))
    return
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/adversarials/core/consts.py
# Compiled at: 2018-12-21 01:06:52
# Size of source mod 2**32: 2511 bytes
__doc__ = 'Constants for Adversarial package.\n\n   @author\n     Victor I. Afolabi\n     Artificial Intelligence Expert & Software Engineer.\n     Email: javafolabi@gmail.com | victor.afolabi@zephyrtel.com\n     GitHub: https://github.com/victor-iyiola\n\n   @project\n     File: consts.py\n     Created on 20 December, 2018 @ 07:03 PM.\n\n   @license\n     MIT License\n     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.\n'
import os.path
from adversarials.core import Config
__all__ = [
 'FS', 'SETUP', 'LOGGER']

class FS:
    PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    APP_NAME = os.path.basename(PROJECT_DIR)
    ASSET_DIR = os.path.join(PROJECT_DIR, 'assets')
    CACHE_DIR = os.path.join(ASSET_DIR, 'cache')
    MODEL_DIR = os.path.join(CACHE_DIR, 'models')


class SETUP:
    _SETUP__global = Config.from_cfg(os.path.join(FS.PROJECT_DIR, 'adversarials/config/', 'setup/global.cfg'))
    MODE = _SETUP__global['config']['MODE']


class LOGGER:
    ROOT = os.path.join(FS.PROJECT_DIR, 'adversarials/config/logger', f"{SETUP.MODE}.cfg")
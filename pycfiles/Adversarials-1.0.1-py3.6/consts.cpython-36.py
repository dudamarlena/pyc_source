# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/adversarials/core/consts.py
# Compiled at: 2018-12-21 01:06:52
# Size of source mod 2**32: 2511 bytes
"""Constants for Adversarial package.

   @author
     Victor I. Afolabi
     Artificial Intelligence Expert & Software Engineer.
     Email: javafolabi@gmail.com | victor.afolabi@zephyrtel.com
     GitHub: https://github.com/victor-iyiola

   @project
     File: consts.py
     Created on 20 December, 2018 @ 07:03 PM.

   @license
     MIT License
     Copyright (c) 2018. Victor I. Afolabi. All rights reserved.
"""
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
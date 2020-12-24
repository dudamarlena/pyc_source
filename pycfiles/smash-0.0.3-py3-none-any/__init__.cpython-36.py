# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\dev\projects\philipov\smash\smash\templates\__init__.py
# Compiled at: 2017-09-23 11:15:29
# Size of source mod 2**32: 928 bytes
"""
global constants
"""
from pathlib import Path
TEMPLATES_ROOT = Path(__file__).parents[0]
ROOT_YAMLISP = '__root__.yml'
ENV_YAMLISP = '__env__.yml'
PKG_YAMLISP = '__pkg__.yml'
STOP_FILE = TEMPLATES_ROOT / '__stop__'
SMASH_PY = TEMPLATES_ROOT / 'smash.py'
SMASH_SPEC = TEMPLATES_ROOT / 'smash.spec'
INSTANCE_CONFIG = TEMPLATES_ROOT / 'instance' / ROOT_YAMLISP
ENV_CONFIG = TEMPLATES_ROOT / 'instance' / ENV_YAMLISP
PKG_CONFIG = TEMPLATES_ROOT / 'instance' / PKG_YAMLISP
NIX_HOST = TEMPLATES_ROOT / 'host-nix'
WIN_HOST = TEMPLATES_ROOT / 'host-win'
NET = TEMPLATES_ROOT / 'net'
PYTHON = TEMPLATES_ROOT / 'python'
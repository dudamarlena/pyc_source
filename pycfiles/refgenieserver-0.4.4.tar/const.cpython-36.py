# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/mstolarczyk/Uczelnia/UVA/code/refgenieserver/refgenieserver/const.py
# Compiled at: 2020-01-15 10:22:43
# Size of source mod 2**32: 1106 bytes
""" Package constants """
import os
from refgenconf.const import *
from refgenconf._version import __version__ as rgc_v
from ._version import __version__ as server_v
from platform import python_version
ALL_VERSIONS = {'server_version':server_v,  'rgc_version':rgc_v,  'python_version':python_version()}
PKG_NAME = 'refgenieserver'
DEFAULT_PORT = 80
BASE_DIR = '/genomes'
TEMPLATES_DIRNAME = 'templates'
TEMPLATES_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), TEMPLATES_DIRNAME)
STATIC_DIRNAME = 'static'
STATIC_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), STATIC_DIRNAME)
LOG_FORMAT = '%(levelname)s in %(funcName)s: %(message)s'
MSG_404 = 'No such {} on server'
DESC_PLACEHOLDER = 'No description'
CHECKSUM_PLACEHOLDER = 'No digest'
CHANGED_KEYS = {CFG_ASSET_PATH_KEY: 'path'}
# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/snipsmanager/__init__.py
# Compiled at: 2017-12-14 05:50:14
""" snipsmanager module """
__version__ = '0.1.6.42'
import os, logging, subprocess, sys

def which(command, default_value):
    try:
        return subprocess.check_output(['which', command]).strip()
    except subprocess.CalledProcessError:
        return default_value


HOME_DIR = os.path.expanduser('~')
if 'arm' in (' ').join(os.uname()):
    HOME_DIR = '/home/pi'
PACKAGE_NAME = 'snipsmanager'
SNIPS_CACHE_DIR_NAME = '.snips'
SNIPS_CACHE_DIR = os.path.join(HOME_DIR, SNIPS_CACHE_DIR_NAME)
NODE_MODULES_PARENT_DIR = SNIPS_CACHE_DIR
NODE_MODULES_DIR = os.path.join(NODE_MODULES_PARENT_DIR, 'node_modules')
DEFAULT_SNIPSFILE_PATH = os.path.join(os.getcwd(), 'Snipsfile')
SNIPS_CACHE_INTENTS_DIR = os.path.join(SNIPS_CACHE_DIR, 'intents')
SNIPS_CACHE_INTENT_REGISTRY_FILE = os.path.join(SNIPS_CACHE_INTENTS_DIR, 'intent_registry.py')
ASOUNDCONF_DEST_PATH = '/etc/asound.conf'
SHELL_COMMAND = which('bash', '/bin/bash')
this_dir, this_filename = os.path.split(__file__)
__DEB_VENV = ('/opt/venvs/{}').format(PACKAGE_NAME)
if this_dir.startswith(__DEB_VENV):
    VENV_PATH = __DEB_VENV
    PIP_BINARY = os.path.join(VENV_PATH, 'bin/pip')
elif 'VIRTUAL_ENV' in os.environ:
    VENV_PATH = os.environ['VIRTUAL_ENV']
    PIP_BINARY = os.path.join(VENV_PATH, 'bin/pip')
else:
    VENV_PATH = None
    PIP_BINARY = which('pip', '/usr/local/bin/pip')

def prepare_cache():
    if not os.path.exists(HOME_DIR):
        os.makedirs(HOME_DIR)
    if not os.path.exists(SNIPS_CACHE_DIR):
        os.makedirs(SNIPS_CACHE_DIR)


prepare_cache()
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
log_format = '\x1b[2m%(asctime)s\x1b[0m [%(levelname)s] %(message)s'
date_format = '%Y-%m-%d %H:%M:%S'
formatter = logging.Formatter(log_format, date_format)
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.INFO)
RESET_SEQ = '\x1b[0m'
GREEN_COLOR = '\x1b[32m'
BLUE_COLOR = '\x1b[34m'
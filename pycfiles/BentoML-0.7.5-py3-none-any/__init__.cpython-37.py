# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/chaoyu/workspace/BentoML/bentoml/configuration/__init__.py
# Compiled at: 2019-12-18 20:21:36
# Size of source mod 2**32: 6350 bytes
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
import os, logging
from pathlib import Path
from bentoml import __version__
from bentoml.utils import _is_pypi_release
from bentoml.exceptions import BentoMLConfigException
from bentoml.configuration.configparser import BentoMLConfigParser
logger = logging.getLogger(__name__)
DEFAULT_CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'default_bentoml.cfg')

def expand_env_var(env_var):
    """Expands potentially nested env var by repeatedly applying `expandvars` and
    `expanduser` until interpolation stops having any effect.
    """
    if not env_var:
        return env_var
    while True:
        interpolated = os.path.expanduser(os.path.expandvars(str(env_var)))
        if interpolated == env_var:
            return interpolated
        env_var = interpolated


def parameterized_config(template):
    """Generates a configuration from the provided template + variables defined in
    current scope

    Args:
        :param template: a config content templated with {{variables}}
    Returns:
        string: config content after templated with locals() and globals()
    """
    all_vars = {k:v for d in [globals(), locals()] for k, v in d.items()}
    return (template.format)(**all_vars)


DEFAULT_BENTOML_HOME = expand_env_var(os.environ.get('BENTOML_HOME', '~/bentoml'))
BENTOML_HOME = DEFAULT_BENTOML_HOME
BENTOML_VERSION = __version__
PREV_PYPI_RELEASE_VERSION = __version__.split('+')[0]
if not _is_pypi_release():
    BENTOML_VERSION = PREV_PYPI_RELEASE_VERSION

def get_local_config_file():
    global BENTOML_HOME
    if 'BENTOML_CONFIG' in os.environ:
        return expand_env_var(os.environ.get('BENTOML_CONFIG'))
    return os.path.join(BENTOML_HOME, 'bentoml.cfg')


def load_config():
    try:
        Path(BENTOML_HOME).mkdir(exist_ok=True)
    except OSError as err:
        try:
            raise BentoMLConfigException("Error creating bentoml home directory '{}': {}".format(BENTOML_HOME, err.strerror))
        finally:
            err = None
            del err

    with open(DEFAULT_CONFIG_FILE, 'rb') as (f):
        DEFAULT_CONFIG = f.read().decode('utf-8')
    loaded_config = BentoMLConfigParser(default_config=(parameterized_config(DEFAULT_CONFIG)))
    local_config_file = get_local_config_file()
    if os.path.isfile(local_config_file):
        logger.info('Loading local BentoML config file: %s', local_config_file)
        with open(local_config_file, 'rb') as (f):
            loaded_config.read_string(parameterized_config(f.read().decode('utf-8')))
    else:
        logger.info('No local BentoML config file found, using default configurations')
    return loaded_config


_config = None

def _reset_bentoml_home(new_bentoml_home_directory):
    global BENTOML_HOME
    global DEFAULT_BENTOML_HOME
    global _config
    DEFAULT_BENTOML_HOME = new_bentoml_home_directory
    BENTOML_HOME = new_bentoml_home_directory
    _config = load_config()
    from bentoml.utils.log import configure_logging
    root = logging.getLogger()
    map(root.removeHandler, root.handlers[:])
    map(root.removeFilter, root.filters[:])
    configure_logging()


def _get_bentoml_home():
    return BENTOML_HOME


def config(section=None):
    global _config
    if _config is None:
        _config = load_config()
    if section is not None:
        return _config[section]
    return _config


def get_bentoml_deploy_version():
    """
    BentoML version to use for generated docker image or serverless function bundle to
    be deployed, this can be changed to an url to your fork of BentoML on github, or an
    url to your custom BentoML build, for example:

    bentoml_deploy_version = git+https://github.com/{username}/bentoml.git@{branch}
    """
    bentoml_deploy_version = config('core').get('bentoml_deploy_version')
    if bentoml_deploy_version != __version__:
        logger.warning("BentoML local changes detected - Local BentoML repository including all code changes will be bundled together with the BentoService bundle. When used with docker, the base docker image will be default to same version as last PyPI release at version: %s. You can also force bentoml to use a specific version for deploying your BentoService bundle, by setting the config 'core/bentoml_deploy_version' to a pinned version or your custom BentoML on github, e.g.:'bentoml_deploy_version = git+https://github.com/{username}/bentoml.git@{branch}'", PREV_PYPI_RELEASE_VERSION)
    return bentoml_deploy_version
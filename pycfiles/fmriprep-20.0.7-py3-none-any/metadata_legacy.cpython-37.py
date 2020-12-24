# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_internal/operations/build/metadata_legacy.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 2011 bytes
"""Metadata generation logic for legacy source distributions.
"""
import logging, os
from pip._internal.exceptions import InstallationError
from pip._internal.utils.setuptools_build import make_setuptools_egg_info_args
from pip._internal.utils.subprocess import call_subprocess
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from pip._internal.build_env import BuildEnvironment
logger = logging.getLogger(__name__)

def _find_egg_info(directory):
    """Find an .egg-info subdirectory in `directory`.
    """
    filenames = [f for f in os.listdir(directory) if f.endswith('.egg-info')]
    if not filenames:
        raise InstallationError('No .egg-info directory found in {}'.format(directory))
    if len(filenames) > 1:
        raise InstallationError('More than one .egg-info directory found in {}'.format(directory))
    return os.path.join(directory, filenames[0])


def generate_metadata(build_env, setup_py_path, source_dir, isolated, details):
    """Generate metadata using setup.py-based defacto mechanisms.

    Returns the generated metadata directory.
    """
    logger.debug('Running setup.py (path:%s) egg_info for package %s', setup_py_path, details)
    egg_info_dir = TempDirectory(kind='pip-egg-info',
      globally_managed=True).path
    args = make_setuptools_egg_info_args(setup_py_path,
      egg_info_dir=egg_info_dir,
      no_user_config=isolated)
    with build_env:
        call_subprocess(args,
          cwd=source_dir,
          command_desc='python setup.py egg_info')
    return _find_egg_info(egg_info_dir)
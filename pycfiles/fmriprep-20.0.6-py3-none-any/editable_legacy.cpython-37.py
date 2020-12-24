# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_internal/operations/install/editable_legacy.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 1488 bytes
"""Legacy editable installation process, i.e. `setup.py develop`.
"""
import logging
from pip._internal.utils.logging import indent_log
from pip._internal.utils.setuptools_build import make_setuptools_develop_args
from pip._internal.utils.subprocess import call_subprocess
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import List, Optional, Sequence
    from pip._internal.build_env import BuildEnvironment
logger = logging.getLogger(__name__)

def install_editable(install_options, global_options, prefix, home, use_user_site, name, setup_py_path, isolated, build_env, unpacked_source_directory):
    """Install a package in editable mode. Most arguments are pass-through
    to setuptools.
    """
    logger.info('Running setup.py develop for %s', name)
    args = make_setuptools_develop_args(setup_py_path,
      global_options=global_options,
      install_options=install_options,
      no_user_config=isolated,
      prefix=prefix,
      home=home,
      use_user_site=use_user_site)
    with indent_log():
        with build_env:
            call_subprocess(args,
              cwd=unpacked_source_directory)
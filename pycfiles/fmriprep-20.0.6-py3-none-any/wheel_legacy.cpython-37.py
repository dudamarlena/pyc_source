# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-92t6atcz/pip/pip/_internal/operations/build/wheel_legacy.py
# Compiled at: 2020-04-16 14:32:20
# Size of source mod 2**32: 3349 bytes
import logging, os.path
from pip._internal.utils.setuptools_build import make_setuptools_bdist_wheel_args
from pip._internal.utils.subprocess import LOG_DIVIDER, call_subprocess, format_command_args
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.utils.ui import open_spinner
if MYPY_CHECK_RUNNING:
    from typing import List, Optional, Text
logger = logging.getLogger(__name__)

def format_command_result(command_args, command_output):
    """Format command information for logging."""
    command_desc = format_command_args(command_args)
    text = 'Command arguments: {}\n'.format(command_desc)
    if not command_output:
        text += 'Command output: None'
    else:
        if logger.getEffectiveLevel() > logging.DEBUG:
            text += 'Command output: [use --verbose to show]'
        else:
            if not command_output.endswith('\n'):
                command_output += '\n'
            text += 'Command output:\n{}{}'.format(command_output, LOG_DIVIDER)
    return text


def get_legacy_build_wheel_path(names, temp_dir, name, command_args, command_output):
    """Return the path to the wheel in the temporary build directory."""
    names = sorted(names)
    if not names:
        msg = 'Legacy build of wheel for {!r} created no files.\n'.format(name)
        msg += format_command_result(command_args, command_output)
        logger.warning(msg)
        return
    if len(names) > 1:
        msg = 'Legacy build of wheel for {!r} created more than one file.\nFilenames (choosing first): {}\n'.format(name, names)
        msg += format_command_result(command_args, command_output)
        logger.warning(msg)
    return os.path.join(temp_dir, names[0])


def build_wheel_legacy(name, setup_py_path, source_dir, global_options, build_options, tempd):
    """Build one unpacked package using the "legacy" build process.

    Returns path to wheel if successfully built. Otherwise, returns None.
    """
    wheel_args = make_setuptools_bdist_wheel_args(setup_py_path,
      global_options=global_options,
      build_options=build_options,
      destination_dir=tempd)
    spin_message = 'Building wheel for %s (setup.py)' % (name,)
    with open_spinner(spin_message) as (spinner):
        logger.debug('Destination directory: %s', tempd)
        try:
            output = call_subprocess(wheel_args,
              cwd=source_dir,
              spinner=spinner)
        except Exception:
            spinner.finish('error')
            logger.error('Failed building wheel for %s', name)
            return
        else:
            names = os.listdir(tempd)
            wheel_path = get_legacy_build_wheel_path(names=names,
              temp_dir=tempd,
              name=name,
              command_args=wheel_args,
              command_output=output)
            return wheel_path
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/main.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 1359 bytes
"""Primary application entrypoint.
"""
from __future__ import absolute_import
import locale, logging, os, sys
from pip._internal.cli.autocompletion import autocomplete
from pip._internal.cli.main_parser import parse_command
from pip._internal.commands import create_command
from pip._internal.exceptions import PipError
from pip._internal.utils import deprecation
logger = logging.getLogger(__name__)

def main(args=None):
    if args is None:
        args = sys.argv[1:]
    deprecation.install_warning_logger()
    autocomplete()
    try:
        cmd_name, cmd_args = parse_command(args)
    except PipError as exc:
        sys.stderr.write('ERROR: %s' % exc)
        sys.stderr.write(os.linesep)
        sys.exit(1)

    try:
        locale.setlocale(locale.LC_ALL, '')
    except locale.Error as e:
        logger.debug('Ignoring error %s when setting locale', e)

    command = create_command(cmd_name, isolated=('--isolated' in cmd_args))
    return command.main(cmd_args)
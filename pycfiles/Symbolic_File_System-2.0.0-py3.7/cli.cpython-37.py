# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sfs/cli.py
# Compiled at: 2018-12-30 12:34:42
# Size of source mod 2**32: 2664 bytes
"""
CLI module for SFS
This module is responsible for bootstrapping the application and executing the CLI
"""
import argparse, contextlib, sys
import sfs.events as events
import sfs.exceptions as exceptions
import sfs.log_utils as log
import sfs.ops as ops
error_messages = {'VALIDATION':'Invalid Command:', 
 'INTERNAL':'Internal Error: ', 
 'UNKNOWN':'Unknown error occurred'}
parser = argparse.ArgumentParser(prog='sfs',
  description='Symbolic File System for backing up, organizing your data and more')
parser.add_argument('-v',
  '--verbose', action='store_true',
  help='Get a verbose output')
command_subparsers = parser.add_subparsers(dest='command',
  title='SFS Commands',
  description='List of all available SFS commands')
command_subparsers.required = True

@contextlib.contextmanager
def cli_manager(command=None, exit_on_error=True, raise_error=False):
    """
    Provides a context for processing parsed CLI commands while catching and handling exceptions
    :param command: Command list to be forwarded to argparse. If None, system arguments are used
    :param exit_on_error: If True, process exits on error
    :param raise_error: If True, caught exception is raised
    """
    error = False
    args = parser.parse_args() if command is None else parser.parse_args(command)
    try:
        try:
            yield args
        except exceptions.CLIValidationException as exc:
            try:
                log.cli_output('{} {}'.format(error_messages['VALIDATION'], str(exc)))
                error = True
            finally:
                exc = None
                del exc

        except exceptions.SFSException as exc:
            try:
                log.cli_output('{} {}'.format(error_messages['INTERNAL'], str(exc)))
                log.logger.exception('Internal Error')
                error = True
            finally:
                exc = None
                del exc

        except Exception:
            log.cli_output(error_messages['UNKNOWN'])
            log.logger.exception('Unknown Error')
            error = True

    finally:
        if error:
            if raise_error:
                raise
        if exit_on_error:
            sys.exit(1 if error else 0)


def exec_cli():
    """Executes the CLI when this module is run as a script"""
    ops.import_ops()
    events.invoke_subscribers((events.events['CLI_REGISTRY']), command_subparsers, parents=[])
    with cli_manager() as (args):
        if args.verbose:
            log.cli_handler.setLevel('DEBUG')
        events.invoke_subscribers(events.command_key(args.command), args)
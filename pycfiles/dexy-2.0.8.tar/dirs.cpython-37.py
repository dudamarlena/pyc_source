# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/ana/dev/dexy-clean/dexy/commands/dirs.py
# Compiled at: 2020-03-18 15:12:33
# Size of source mod 2**32: 1451 bytes
from dexy.commands.utils import init_wrapper
from dexy.utils import defaults

def reset_command(__cli_options=False, artifactsdir=defaults['artifacts_dir'], logdir=defaults['log_dir']):
    """
    Clean out the contents of dexy's cache and reports directories.
    """
    wrapper = init_wrapper(locals())
    wrapper.remove_dexy_dirs()
    wrapper.remove_reports_dirs(keep_empty_dir=True)
    wrapper.create_dexy_dirs()


def build_reset_parser(parser):
    parser.set_defaults(cmd=reset_command)
    parser.add_argument('--artifacts_dir', defaults['artifacts_dir'])


def cleanup_command(__cli_options=False, artifactsdir=defaults['artifacts_dir'], logdir=defaults['log_dir'], reports=True):
    """
    Remove the directories which dexy created, including working directories
    and reports.
    """
    wrapper = init_wrapper(locals())
    wrapper.remove_dexy_dirs()
    wrapper.remove_reports_dirs(reports)


def setup_command(__cli_options=False, artifactsdir=defaults['artifacts_dir'], **kwargs):
    """
    Create the directories dexy needs to run.
    """
    wrapper = init_wrapper(locals())
    wrapper.create_dexy_dirs()
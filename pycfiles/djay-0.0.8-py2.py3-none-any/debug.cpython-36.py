# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-sin1koo5/pip/pip/_internal/commands/debug.py
# Compiled at: 2019-07-30 18:46:55
# Size of source mod 2**32: 3360 bytes
from __future__ import absolute_import
import locale, logging, sys
from pip._internal.cli import cmdoptions
from pip._internal.cli.base_command import Command
from pip._internal.cli.cmdoptions import make_target_python
from pip._internal.cli.status_codes import SUCCESS
from pip._internal.utils.logging import indent_log
from pip._internal.utils.misc import get_pip_version
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
from pip._internal.wheel import format_tag
if MYPY_CHECK_RUNNING:
    from typing import Any, List
    from optparse import Values
logger = logging.getLogger(__name__)

def show_value(name, value):
    logger.info('{}: {}'.format(name, value))


def show_sys_implementation():
    logger.info('sys.implementation:')
    if hasattr(sys, 'implementation'):
        implementation = sys.implementation
        implementation_name = implementation.name
    else:
        implementation_name = ''
    with indent_log():
        show_value('name', implementation_name)


def show_tags(options):
    tag_limit = 10
    target_python = make_target_python(options)
    tags = target_python.get_tags()
    formatted_target = target_python.format_given()
    suffix = ''
    if formatted_target:
        suffix = ' (target: {})'.format(formatted_target)
    else:
        msg = 'Compatible tags: {}{}'.format(len(tags), suffix)
        logger.info(msg)
        if options.verbose < 1:
            if len(tags) > tag_limit:
                tags_limited = True
                tags = tags[:tag_limit]
        tags_limited = False
    with indent_log():
        for tag in tags:
            logger.info(format_tag(tag))

        if tags_limited:
            msg = '...\n[First {tag_limit} tags shown. Pass --verbose to show all.]'.format(tag_limit=tag_limit)
            logger.info(msg)


class DebugCommand(Command):
    __doc__ = '\n    Display debug information.\n    '
    name = 'debug'
    usage = '\n      %prog <options>'
    summary = 'Show information useful for debugging.'
    ignore_require_venv = True

    def __init__(self, *args, **kw):
        (super(DebugCommand, self).__init__)(*args, **kw)
        cmd_opts = self.cmd_opts
        cmdoptions.add_target_python_options(cmd_opts)
        self.parser.insert_option_group(0, cmd_opts)

    def run(self, options, args):
        logger.warning('This command is only meant for debugging. Do not use this with automation for parsing and getting these details, since the output and options of this command may change without notice.')
        show_value('pip version', get_pip_version())
        show_value('sys.version', sys.version)
        show_value('sys.executable', sys.executable)
        show_value('sys.getdefaultencoding', sys.getdefaultencoding())
        show_value('sys.getfilesystemencoding', sys.getfilesystemencoding())
        show_value('locale.getpreferredencoding', locale.getpreferredencoding())
        show_value('sys.platform', sys.platform)
        show_sys_implementation()
        show_tags(options)
        return SUCCESS
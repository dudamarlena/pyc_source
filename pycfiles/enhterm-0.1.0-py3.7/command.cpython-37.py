# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\command.py
# Compiled at: 2019-11-09 02:55:31
# Size of source mod 2**32: 3765 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging, shlex, traceback
from collections import OrderedDict
from .lang import _
logger = logging.getLogger('enhterm')

class CommandMixin(object):
    __doc__ = '\n    Extends normal command processing by allowing strings to be executes.\n\n    Depends on MessagesMixin.\n    '

    def __init__(self, *args, **kwargs):
        (super(CommandMixin, self).__init__)(*args, **kwargs)

    def cmd_with_result(self, line):
        """Interpret the argument as if it had been typed in response
        to the prompt.
        """
        prefix = 'do_'
        cmd, arg, line = self.parseline(str(line))
        if not line:
            return (
             self.emptyline(), False)
        if cmd is None:
            return (
             self.default(line), False)
        self.lastcmd = line
        if line == 'EOF':
            self.lastcmd = ''
        if cmd == '':
            return (
             self.default(line), False)
        try:
            shortcut = self.shortcuts[cmd]
            cmd = shortcut[0]
            arg = '%s %s' % (shortcut[1], arg)
        except KeyError:
            pass

        try:
            cmd, arg = self.get_subcommand(cmd, arg)
            prefix = 'sdo_'
        except KeyError:
            pass
        except RuntimeError as exc:
            try:
                self.error(str(exc))
                return (False, False)
            finally:
                exc = None
                del exc

        try:
            func = getattr(self, prefix + cmd)
        except AttributeError:
            return (
             self.default(line), False)
        else:
            if cmd == 'help':
                return (
                 self.do_help(arg), False)
            try:
                args_template = getattr(self, 'args_' + cmd)
            except AttributeError:
                args_template = [
                 'args']

            try:
                parsed = parse(arg, args_template)
            except ValueError as exc:
                try:
                    self.error(_('Arguments could not be parsed:'), str(exc))
                    return (False, False)
                finally:
                    exc = None
                    del exc

            try:
                return (
                 func(parsed), True)
            except Exception as exc:
                try:
                    self.error(_('Exception while executing do_%s') % cmd, str(exc))
                    traceback.print_exc(file=(self.stdout))
                    return (False, False)
                finally:
                    exc = None
                    del exc


def parse(args, args_template=None):
    """Interprets arguments based on input"""
    args = shlex.split(args)
    if args_template is None:
        return OrderedDict(((k, None) for k in args))
    result = OrderedDict()
    has_args = 'args' in args_template
    i = 0
    missing = ''
    for templ in args_template:
        if templ == 'args':
            continue
        try:
            result[templ] = args[i]
            i = i + 1
        except IndexError:
            missing = missing + _('Required argument %s is missing\n') % templ

    if len(missing):
        raise ValueError(missing)
    elif i < len(args):
        if has_args:
            result['args'] = args[i:]
        else:
            raise ValueError(_('Unrecognized arguments: ') + ', '.join(args[i:]))
    elif has_args:
        result['args'] = []
    return result
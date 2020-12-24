# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\subcommand.py
# Compiled at: 2019-11-09 03:05:36
# Size of source mod 2**32: 3115 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
from .lang import _
logger = logging.getLogger('enhterm')

class SubcommandMixin(object):
    __doc__ = '\n    Infrastructure for sub-commands.\n    '
    subcommands = {}

    def __init__(self, *args, **kwargs):
        (super(SubcommandMixin, self).__init__)(*args, **kwargs)

    def add_subcommand(self, command, subcommand, callable=None):
        """
        Add a sub-command.

        Arguments:
        ----------

        command : string or list
            Can be either a path or a single string (
            will be converted in a path with a single element).
        subcommand : string
            The final element of the path.
        callable : string
            The name of the function to call.
        """
        if not isinstance(command, (list, set, tuple)):
            command = (
             command,)
        else:
            the_store = self.subcommands
            traceme = ''
            for cmnditr in command:
                try:
                    dive = the_store[cmnditr]
                except KeyError:
                    dive = {}
                    the_store[cmnditr] = dive

                traceme = '%s_%s' % (traceme, cmnditr) if len(traceme) else cmnditr
                the_store = dive

            if callable is None:
                callable = '%s_%s' % (traceme, subcommand)
            try:
                the_store[subcommand] = callable
            except KeyError:
                the_store[subcommand] = {subcommand: callable}

    def get_subcommand(self, command, args):
        missing_is_error = False
        traceme = ''
        the_store = self.subcommands
        while True:
            traceme = '%s_%s' % (traceme, command) if len(traceme) else command
            try:
                subcommands = the_store[command]
            except KeyError as exc:
                try:
                    if missing_is_error:
                        raise RuntimeError(_('Command <%s> is not defined') % traceme)
                    else:
                        raise exc
                finally:
                    exc = None
                    del exc

            if isinstance(subcommands, str):
                return (
                 subcommands, args)
            the_store = subcommands
            if len(args) == 0:
                raise RuntimeError(_('Command <%s> needs a subcommand') % traceme)
            command, args, line = self.parseline(args)

    def print_subcommands(self):
        """Informs the user about available subcommands."""

        def recursive(indent, value):
            for kkk in value:
                self.info_line('%s%s' % (indent, kkk))
                newval = value[kkk]
                if not isinstance(newval, str):
                    recursive(indent + '  ', newval)

        recursive('', self.subcommands)
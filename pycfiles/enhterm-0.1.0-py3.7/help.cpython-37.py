# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\help.py
# Compiled at: 2019-11-09 02:45:51
# Size of source mod 2**32: 2450 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import cmd, logging
from .lang import _
logger = logging.getLogger('enhterm')

class HelpMixin(object):
    __doc__ = '\n    Extends normal help command output.\n    '

    def __init__(self, *args, **kwargs):
        (super(HelpMixin, self).__init__)(*args, **kwargs)

    def do_help(self, arg):
        """
        List available commands with "help" or detailed help with "help cmd".
        """

        def help_attempt(name, tag_help='help_', tag_do='do_'):
            try:
                func = getattr(self, tag_help + name)
            except AttributeError:
                try:
                    doc = getattr(self, tag_do + name).__doc__
                    if doc:
                        self.print_message('%s\n' % str(doc))
                        return True
                except AttributeError:
                    pass

                return False
            else:
                func()
                return True

        if arg:
            help_attempt(arg) or help_attempt((arg.replace('  ', ' ').replace(' ', '_')),
              tag_help='helps_',
              tag_do='sdo_') or self.print_message('%s\n' % str(self.nohelp % (arg,)))
        else:
            cmd.Cmd.do_help(self, arg)
        if len(arg) == 0:
            if len(self.subcommands) > 0:
                self.info_start(_('SUB-COMMANDS:\n============'))
                self.print_subcommands()
                self.info_end(_('\n\n'))
            else:
                if len(self.shortcuts) > 0:
                    self.info_start(_('SHORTCUTS:\n=========='))
                    for k in self.shortcuts:
                        self.info_line(_('   %-16s  %s') % (
                         k, ' '.join(self.shortcuts[k])))

                    self.info_end(_(''))
                try:
                    getattr(self, 'help_getting_started')
                    self.info(_("Type 'help getting started' to see a step-by-step introduction"))
                except AttributeError:
                    pass
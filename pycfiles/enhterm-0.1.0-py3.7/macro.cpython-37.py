# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\enhterm\macro.py
# Compiled at: 2019-11-09 02:48:41
# Size of source mod 2**32: 6873 bytes
"""
"""
from __future__ import unicode_literals
from __future__ import print_function
import logging
from collections import OrderedDict
from .util import needs_name
from .lang import _
logger = logging.getLogger('enhterm')

class MacroMixin(object):
    __doc__ = '\n    Allows the user to record and playback macros.\n    '

    def __init__(self, *args, **kwargs):
        (super(MacroMixin, self).__init__)(*args, **kwargs)
        self.shortcuts['m'] = ('run', 'macro')
        self.add_subcommand('new', 'macro')
        self.add_subcommand('end', 'macro')
        self.add_subcommand('run', 'macro')
        self.add_subcommand('drop', 'macro')
        self.add_subcommand('list', 'macros')
        self.macros = OrderedDict()
        self.macro_recording = None
        self.macro_rec_name = None

    @property
    def is_macro_recording(self):
        """Tells if we're currently recording"""
        return self.macro_recording is not None

    def command_hook(self, line):
        """Gets called for every command we execute"""
        if self.is_macro_recording:
            self.macro_recording.append(line)

    args_new_macro = ['name']

    @needs_name
    def sdo_new_macro(self, arg, name):
        """
        Starts recording a new macro.

        Parameters
        ----------

        name : string
            A name for the macro. You will use
            this to later recall the macro.

        """
        if self.is_macro_recording:
            raise RuntimeError(_('Already recording macro %s') % repr(self.macro_rec_name))
        self.macro_rec_name = name
        self.macro_recording = []

    def helps_new_macro(self):
        self.info(_('\n    Creates a new macro and starts recording.\n\n    Arguments\n    ---------\n    name:     the unique identifier of the macro.\n\n    Description\n    -----------\n    Macros are stored at instance level and are available\n    to all agents.\n\n    Example\n    -------\n    $: new macro cmd1\n    '))

    args_drop_macro = [
     'name']

    @needs_name
    def sdo_drop_macro(self, arg, name):
        """
        Removes a macro.

        Parameters
        ----------

        name : string
            The name of the macro to delete.

        """
        try:
            del self.macros[name]
        except KeyError:
            self.error(_('Macro `%s` does not exist') % name, _('Use <list macros> command to find out available macros'))

    def helps_drop_macro(self):
        self.info(_('\n    Removes a macro.\n\n    Arguments\n    ---------\n    name:     the unique identifier of the macro.\n\n    Preconditions\n    -------------\n    The macro MUST exist.\n\n    Description\n    -----------\n    Macros are stored at instance level and are available\n    to all agents.\n\n    Example\n    -------\n    $: drop macro cmd1\n    '))

    args_end_macro = []

    def sdo_end_macro(self, arg):
        """
        Ends recording a new macro.

        Parameters
        ----------

        """
        if not self.is_macro_recording:
            raise RuntimeError(_('Not recording a macro'))
        self.macros[self.macro_rec_name] = self.macro_recording[1:]
        self.macro_rec_name = None
        self.macro_recording = None

    def helps_end_macro(self):
        self.info(_('\n    Stops recording and saves the macro.\n\n    Preconditions\n    -------------\n    A record MUST be in the recording stage.\n\n    Description\n    -----------\n    Macros are stored at instance level and are available\n    to all agents.\n\n    Example\n    -------\n    $: end macro\n    '))

    args_list_macros = [
     'args']

    def sdo_list_macros(self, arg):
        """
        Lists available macros.

        Parameters
        ----------

        content : bool
            (optional, default: False) Show the content of the macros.
        arg : dict
            Other arguments
        """
        if len(arg['args']) > 1:
            self.error(_('Too many arguments for command'), _('The format is `list macros [content]`\n  The `content` optional parameter can be \n  true of false (default).'))
            return
        else:
            show_content = False
            if len(arg['args']) == 1:
                show_content = arg['args'][0].lower()
                if show_content in ('true', 'yes', 'on'):
                    show_content = True
            else:
                if show_content in ('false', 'no', 'off'):
                    pass
                else:
                    self.error(_('Invalid argument for command'), _('The format is `list macros [content]`\n  The `content` optional parameter can be \n  true of false (default).'))
                    return
                self.info_start(_('MACROS\n======\n'))
                if len(self.macros) == 0:
                    self.info_line("No macros have been defined. Use 'new macro <name>' to start recording one and 'end macro' to save it.")
                else:
                    for mmm in self.macros:
                        self.info_line('    %s' % mmm)
                        if show_content:
                            for line in self.macros[mmm]:
                                self.info_line('      %s' % line)

        self.info_end('')

    def helps_list_macros(self):
        self.info(_('\n    Lists existing macro.\n\n    Description\n    -----------\n    Macros are stored at instance level and are available\n    to all agents.\n\n    Example\n    -------\n    $: list macros\n    '))

    args_run_macro = [
     'name']

    @needs_name
    def sdo_run_macro(self, arg, name):
        """
        Executes a previously recorded macro

        Parameters
        ----------

        name : string
            The name of the macro to run.

        """
        try:
            commands = self.macros[name]
        except KeyError:
            self.error(_('Macro `%s` does not exist') % name, _('Use <list macros> command to find out available macros'))
            return
        else:
            self.run_commands(commands)

    def helps_run_macro(self):
        self.info(_('\n    Executes a macro.\n\n    Preconditions\n    -------------\n    The macro MUST exist.\n\n    Description\n    -----------\n    Macros are stored at instance level and are available\n    to all agents.\n\n    Example\n    -------\n    $: run macro cmd1\n    '))
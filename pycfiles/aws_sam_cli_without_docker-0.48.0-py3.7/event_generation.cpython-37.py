# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.15-x86_64/egg/samcli/commands/local/generate_event/event_generation.py
# Compiled at: 2020-03-21 12:32:11
# Size of source mod 2**32: 7102 bytes
"""
Generates the services and commands for selection in SAM CLI generate-event
"""
import functools, click
import samcli.lib.generated_sample_events.events as events
from samcli.cli.cli_config_file import TomlProvider, get_ctx_defaults
from samcli.cli.options import debug_option
from samcli.lib.telemetry.metrics import track_command
import samcli.lib.config.samconfig as samconfig

class ServiceCommand(click.MultiCommand):
    __doc__ = '\n    Top level command that defines the service provided\n\n    Methods\n    ----------------\n    get_command(self, ctx, cmd_name):\n        Get the subcommand(s) under a given service name.\n    list_commands(self, ctx):\n        List all of the subcommands\n    '

    def __init__(self, events_lib, *args, **kwargs):
        (super(ServiceCommand, self).__init__)(*args, **kwargs)
        if not events_lib:
            raise ValueError('Events library is necessary to run this command')
        self.events_lib = events_lib
        self.all_cmds = self.events_lib.event_mapping

    def get_command(self, ctx, cmd_name):
        """
        gets the subcommands under the service name

        Parameters
        ----------
        ctx : Context
            the context object passed into the method
        cmd_name : str
            the service name
        Returns
        -------
        EventTypeSubCommand:
            returns subcommand if successful, None if not.
        """
        if cmd_name not in self.all_cmds:
            return
        return EventTypeSubCommand(self.events_lib, cmd_name, self.all_cmds[cmd_name])

    def list_commands(self, ctx):
        """
        lists the service commands available

        Parameters
        ----------
        ctx: Context
            the context object passed into the method
        Returns
        -------
        list
            returns sorted list of the service commands available
        """
        return sorted(self.all_cmds.keys())


class EventTypeSubCommand(click.MultiCommand):
    __doc__ = '\n    Class that describes the commands underneath a given service type\n\n    Methods\n    ----------------\n    get_command(self, ctx, cmd_name):\n        Get the subcommand(s) under a given service name.\n    list_commands(self, ctx):\n        List all of the subcommands\n    '
    TAGS = 'tags'

    def __init__(self, events_lib, top_level_cmd_name, subcmd_definition, *args, **kwargs):
        (super(EventTypeSubCommand, self).__init__)(*args, **kwargs)
        self.top_level_cmd_name = top_level_cmd_name
        self.subcmd_definition = subcmd_definition
        self.events_lib = events_lib

    def get_command(self, ctx, cmd_name):
        """
        gets the Click Commands underneath a service name

        Parameters
        ----------
        ctx: Context
            context object passed in
        cmd_name: string
            the service name
        Returns
        -------
        cmd: Click.Command
            the Click Commands that can be called from the CLI
        """
        if cmd_name not in self.subcmd_definition:
            return
        parameters = []
        for param_name in self.subcmd_definition[cmd_name][self.TAGS].keys():
            default = self.subcmd_definition[cmd_name][self.TAGS][param_name]['default']
            parameters.append(click.Option([
             '--{}'.format(param_name)],
              default=default,
              help=("Specify the {} name you'd like, otherwise the default = {}".format(param_name, default))))

        command_callback = functools.partial(self.cmd_implementation, self.events_lib, self.top_level_cmd_name, cmd_name)
        config = get_ctx_defaults(cmd_name=cmd_name,
          provider=TomlProvider(section='parameters'),
          ctx=ctx,
          config_env_name=(samconfig.DEFAULT_ENV))
        cmd = click.Command(name=cmd_name,
          short_help=(self.subcmd_definition[cmd_name]['help']),
          context_settings={'default_map': config},
          params=parameters,
          callback=command_callback)
        cmd = debug_option(cmd)
        return cmd

    def list_commands(self, ctx):
        """
        lists the commands underneath a particular event

        Parameters
        ----------
        ctx: Context
            the context object passed in
        Returns
        -------
        the sorted list of commands under a service
        """
        return sorted(self.subcmd_definition.keys())

    @track_command
    def cmd_implementation(self, events_lib, top_level_cmd_name, subcmd_name, *args, **kwargs):
        """
        calls for value substitution in the event json and returns the
        customized json as a string

        Parameters
        ----------
        events_lib
        top_level_cmd_name: string
            the name of the service
        subcmd_name: string
            the name of the event under the service
        args: tuple
            any arguments passed in before kwargs
        kwargs: dict
            the keys and values for substitution in the json
        Returns
        -------
        event: string
            returns the customized event json as a string
        """
        event = events_lib.generate_event(top_level_cmd_name, subcmd_name, kwargs)
        click.echo(event)
        return event


class GenerateEventCommand(ServiceCommand):
    __doc__ = '\n    Class that brings ServiceCommand and EventTypeSubCommand into one for easy execution\n    '

    def __init__(self, *args, **kwargs):
        (super(GenerateEventCommand, self).__init__)(events.Events(), *args, **kwargs)
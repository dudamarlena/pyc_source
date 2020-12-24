# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: e:\kanzhun\projects\pycake\src\pycake\options.py
# Compiled at: 2018-11-08 07:12:58
from click import Group, Option, echo
CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])

class PyCakeGroup(Group):
    """Custom Group class provides formatted main help"""

    def get_help_option(self, ctx):
        from .cli_utils import format_help
        help_options = self.get_help_option_names(ctx)
        if not help_options or not self.add_help_option:
            return

        def show_help(ctx, param, value):
            if value and not ctx.resilient_parsing:
                if not ctx.invoked_subcommand:
                    echo(format_help(ctx.get_help()))
                else:
                    echo(ctx.get_help(), color=ctx.color)
                ctx.exit()

        return Option(help_options, is_flag=True, is_eager=True, expose_value=False, callback=show_help, help='Show this message and exit.')
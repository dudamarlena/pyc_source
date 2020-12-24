# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/cli/default_group.py
# Compiled at: 2018-04-09 03:58:38
# Size of source mod 2**32: 2118 bytes
import click, six

class DefaultGroup(click.Group):
    """DefaultGroup"""
    ignore_unknown_options = True

    def __init__(self, *args, **kwargs):
        default_command = kwargs.pop('default_command', None)
        (super(DefaultGroup, self).__init__)(*args, **kwargs)
        self.default_cmd_name = None
        if default_command is not None:
            self.set_default_command(default_command)

    def set_default_command(self, command):
        if isinstance(command, six.string_types):
            cmd_name = command
        else:
            cmd_name = command.name
            self.add_command(command)
        self.default_cmd_name = cmd_name

    def parse_args(self, ctx, args):
        if not args:
            if self.default_cmd_name is not None:
                args.insert(0, self.default_cmd_name)
        return super(DefaultGroup, self).parse_args(ctx, args)

    def get_command(self, ctx, cmd_name):
        if cmd_name not in self.commands:
            if self.default_cmd_name is not None:
                ctx.args0 = cmd_name
                cmd_name = self.default_cmd_name
        return super(DefaultGroup, self).get_command(ctx, cmd_name)

    def resolve_command(self, ctx, args):
        cmd_name, cmd, args = super(DefaultGroup, self).resolve_command(ctx, args)
        args0 = getattr(ctx, 'args0', None)
        if args0 is not None:
            args.insert(0, args0)
        return (cmd_name, cmd, args)
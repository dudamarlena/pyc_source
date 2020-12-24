# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/op_cli/main.py
# Compiled at: 2019-12-06 06:39:57
# Size of source mod 2**32: 1298 bytes
import os, sys, click, re
import op_cli.functions.app as app

@click.group()
@click.version_option('1.0.0')
def main():
    """Command Line API"""
    pass


@main.command()
@click.argument('command', required=False)
def run(**kwargs):
    """Run Command:
        This is a command to run a command api and get a result.

        # Usage

        op-cli run "<command>" - This will run a command api right from the CLI
        op-cli run - This will initiate a repl environment to run the commands
        """
    if kwargs.get('command', None) is None:
        click.echo('Welcome to Command Line API REPL\n')
        while True:
            command = input('Command >>> ')
            res = app.run_command(command)
            click.echo(f"Output  >>> {res} ")

    else:
        res = app.run_command(kwargs.get('command'))
        click.echo(res)


@main.command()
@click.argument('command', required=False)
def commands(**kwargs):
    """
    Command:
    This is a command to get all available command
    """
    if not kwargs.get('command', None):
        res = app.func_map
        res = list(res.keys())
        click.echo(res)
    else:
        res = app.get_command(kwargs.get('command'))
        click.echo(res.__doc__)


if __name__ == '__main__':
    main()
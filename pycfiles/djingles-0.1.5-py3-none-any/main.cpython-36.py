# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/shodh/Projects/djingles/src/djingles/commands/main.py
# Compiled at: 2018-04-19 01:20:30
# Size of source mod 2**32: 212 bytes
import click

@click.group()
@click.option('--debug/--no-debug', default=False)
def cli(debug):
    click.echo(('Debug mode is %s' % ('on' if debug else 'off')), err=True)


if __name__ == '__main__':
    cli()
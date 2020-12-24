# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/shakespearelang/cli.py
# Compiled at: 2019-02-05 20:16:34
# Size of source mod 2**32: 641 bytes
import click
from .shakespeare_interpreter import Shakespeare
from .repl import start_console, debug_play

@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx):
    if ctx.invoked_subcommand is None:
        console()


@main.command()
def console():
    start_console()


@main.command()
@click.argument('file')
def run(file):
    with open(file, 'r') as (f):
        play = f.read()
        interpreter = Shakespeare()
        interpreter.run_play(play)


@main.command()
@click.argument('file')
def debug(file):
    with open(file, 'r') as (f):
        play = f.read()
        debug_play(play)
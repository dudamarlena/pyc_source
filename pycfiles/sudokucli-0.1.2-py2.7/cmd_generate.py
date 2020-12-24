# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\src\commands\cmd_generate.py
# Compiled at: 2018-08-23 04:18:07
import click
from src.cli import pass_context
from src.abs.game import Game

@click.command('generate', short_help='Show a view of 9*9 sudoku map')
@click.option('--coordinate/--no-coordinate', default=True)
@click.option('--check/--no-check', default=True)
@click.option('--mode', type=click.Choice(['easy', 'medium', 'hard', 'extreme']), default='medium')
@pass_context
def cli(ctx, coordinate, check, mode):
    game = Game(with_coordinate=coordinate, step_check=check, mode=mode, random=6, mutiple=18, lmutiple=8)
    game.fill_random()
    game.flush()
    game.gloop()
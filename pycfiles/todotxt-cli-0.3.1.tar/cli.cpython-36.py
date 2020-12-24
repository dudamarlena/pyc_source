# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\faoustin\Workspace\todotxt-cli\todotxt\cli.py
# Compiled at: 2019-10-03 09:32:40
# Size of source mod 2**32: 2294 bytes
from logging import Formatter, Handler, getLogger, NOTSET, INFO, DEBUG, WARNING
import click
level2color = {0:'black', 
 10:'blue', 
 20:'green', 
 30:'yellow', 
 40:'red', 
 50:'magenta'}

class ClickHandler(Handler):

    def __init__(self, level=NOTSET):
        Handler.__init__(self, level)

    def emit(self, record):
        click.echo(click.style((self.format(record)), fg=(level2color.get(record.levelno, 'white'))))


logger = getLogger('todotxt')
ch = ClickHandler()
ch.setLevel(DEBUG)
formatter = Formatter('%(levelname)s - %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

@click.group()
@click.option('-vv', '--verbose', is_flag=True)
@click.option('-c', '--config', type=(click.File('rb')))
@click.version_option('0.1.0')
def cli(verbose, config):
    if verbose:
        logger.setLevel(DEBUG)
    else:
        logger.setLevel(WARNING)


@cli.command()
@click.argument('task', nargs=(-1))
def add(task):
    """
    add task
    """
    task = ' '.join(task)


@cli.command()
@click.argument('idtask', nargs=1)
def rm(idtask):
    """
    remove task
    """
    pass


@cli.command()
@click.option('--now', is_flag=True)
@click.option('--week', is_flag=True)
@click.option('--month', is_flag=True)
@click.option('--day', type=int)
@click.argument('filter', nargs=(-1))
def ls(now, week, month, day, filter):
    """
    list of tasks
    """
    pass


@cli.command()
@click.argument('idtask', nargs=1)
@click.argument('task', nargs=(-1))
def replace(idtask, task):
    """
    replace task
    """
    pass


@cli.command()
@click.argument('idtask', nargs=1)
@click.argument('task', nargs=(-1))
def append(idtask, task):
    """
    append task
    """
    pass


@cli.command()
@click.argument('idtask', nargs=1)
@click.argument('task', nargs=(-1))
def cancel(idtask, task):
    """
    cancel elt in task
    """
    pass


@cli.command()
@click.argument('task', nargs=(-1))
def done(idtask):
    """
    done task
    """
    pass


@cli.command()
@click.argument('task', nargs=(-1))
def undone(idtask):
    """
    undone task
    """
    pass


if __name__ == '__main__':
    cli()
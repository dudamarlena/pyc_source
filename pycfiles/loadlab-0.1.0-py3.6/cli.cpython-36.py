# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-x86_64/egg/loadlab/cli.py
# Compiled at: 2018-09-08 20:13:25
# Size of source mod 2**32: 500 bytes
"""Console script for loadlab."""
import sys, click
from loadlab import LoadLab

@click.group()
def main():
    pass


@click.command()
def jobs():
    click.echo(LoadLab().jobs.get())


@click.command()
def plans():
    click.echo(LoadLab().plans.get())


@click.command()
def sites():
    click.echo(LoadLab().sites.get())


main.add_command(jobs)
main.add_command(plans)
main.add_command(sites)
if __name__ == '__main__':
    sys.exit(main())
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sockspy/cli.py
# Compiled at: 2017-07-29 13:23:34
# Size of source mod 2**32: 285 bytes
"""Console script for sockspy."""
import click
from sockspy import sockspy_main

@click.command()
def main(args=None):
    """Console script for sockspy."""
    click.echo('Starting sockspy...')
    sockspy_main.run()


if __name__ == '__main__':
    main()
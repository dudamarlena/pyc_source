# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/rage4/cli.py
# Compiled at: 2020-01-08 06:08:55
"""Console script for rage4."""
import sys, click

@click.command()
def main(args=None):
    """Console script for rage4."""
    click.echo('Replace this message by putting your code into rage4.cli.main')
    click.echo('See click documentation at https://click.palletsprojects.com/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
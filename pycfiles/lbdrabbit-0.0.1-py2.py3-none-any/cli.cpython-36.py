# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/sanhehu/Documents/GitHub/lbdrabbit-project/lbdrabbit/cli.py
# Compiled at: 2019-09-26 19:05:14
# Size of source mod 2**32: 422 bytes
"""
Console script for lbdrabbit.
"""
import sys, click

@click.command()
def main(args=None):
    """Console script for lbdrabbit."""
    click.echo('Replace this message by putting your code into lbdrabbit.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
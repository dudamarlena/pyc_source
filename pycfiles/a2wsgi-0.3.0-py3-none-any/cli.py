# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/ssbarnea/.pyenv/versions/2.7.14/lib/python2.7/site-packages/a2w/cli.py
# Compiled at: 2018-08-02 09:42:36
__doc__ = 'Console script for a2w.'
import sys, click

@click.command()
def main(args=None):
    """Console script for a2w."""
    click.echo('Replace this message by putting your code into a2w.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
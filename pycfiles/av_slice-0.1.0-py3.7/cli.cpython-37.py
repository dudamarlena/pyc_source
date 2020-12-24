# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/av_slice/cli.py
# Compiled at: 2019-06-11 23:51:07
# Size of source mod 2**32: 416 bytes
"""Console script for av_slice."""
import sys, click

@click.command()
def main(args=None):
    """Console script for av_slice."""
    click.echo('Replace this message by putting your code into av_slice.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
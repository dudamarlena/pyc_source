# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/staff_info/cli.py
# Compiled at: 2018-05-22 08:06:10
# Size of source mod 2**32: 422 bytes
"""Console script for staff_info."""
import sys, click

@click.command()
def main(args=None):
    """Console script for staff_info."""
    click.echo('Replace this message by putting your code into staff_info.cli.main')
    click.echo('See click documentation at http://click.pocoo.org/')
    return 0


if __name__ == '__main__':
    sys.exit(main())
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/app/__init__.py
# Compiled at: 2019-04-09 11:39:55
# Size of source mod 2**32: 351 bytes
import click, webbrowser

@click.command()
@click.option('--tag', '-t', help='add a tag')
def main(tag):
    """
    Open a new dev.to browser tab on the browser
    """
    if tag:
        url = 'https://dev.to/t/{}'.format(tag)
    else:
        url = 'https://dev.to'
    webbrowser.open(url, new=2)


if __name__ == '__main__':
    main()
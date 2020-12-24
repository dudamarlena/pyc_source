# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/nb.py
# Compiled at: 2018-08-30 16:40:11
import webbrowser, click

@click.command()
@click.argument('query')
def cli(query):
    """Nanobrain cli"""
    q = ('+').join(query.split(' '))
    url = ('https://nanobrain.io/compute?q={}').format(q)
    click.echo(('\n\t {}').format(url))
    click.echo('\n\t Opening a default browser...')
    webbrowser.open(url)


if __name__ == '__main__':
    cli()
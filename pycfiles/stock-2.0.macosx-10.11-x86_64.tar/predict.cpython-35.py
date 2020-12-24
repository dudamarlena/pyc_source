# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/cli/predict.py
# Compiled at: 2017-02-05 09:58:32
# Size of source mod 2**32: 297 bytes
import click
from stock import query
from .main import cli, AliasedGroup

@cli.group(cls=AliasedGroup, name='predict')
def c():
    pass


@c.command(help='do')
@click.argument('quandl_code')
def do(**kw):
    result = query.predict(**kw)
    click.echo(result)
    return result
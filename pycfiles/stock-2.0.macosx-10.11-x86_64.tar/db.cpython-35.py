# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.5/site-packages/stock/cli/db.py
# Compiled at: 2017-02-07 09:25:16
# Size of source mod 2**32: 839 bytes
import click
from stock import models, query
from .main import cli, AliasedGroup

@cli.group(cls=AliasedGroup)
def db():
    pass


@db.command(help='Show env')
def env():
    tables = ', '.join(models.engine.table_names())
    summary = 'url: {engine.url}\necho: {engine.echo}\nname: {engine.name}\ntables: {tables}\n'.format(engine=models.engine, tables=tables)
    click.echo(summary)


@db.command(help='Create new all tables')
def create():
    models.create_all()


@db.command(help='Drop all tables')
@click.option('-y', '--yes', is_flag=True, default=False)
def drop(yes):
    if yes or click.confirm('Drop all tables. Are you sure?'):
        models.drop_all()


@db.command(name='quandl_codes', help='Store and show quandl code')
def quandl_codes():
    click.secho(', '.join(c for c in query.quandl_codes()))
# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyutrack/cli/delete.py
# Compiled at: 2017-10-28 23:27:23
# Size of source mod 2**32: 852 bytes
import click
from click import get_current_context
from pyutrack import *
from . import cli

@cli.group()
@click.pass_context
def delete(_):
    """
    delete youtrack resources
    """
    pass


@delete.resultcallback()
def result(result):
    get_current_context().obj.render(result)


@delete.command()
@click.pass_context
@click.argument('id')
def issue(ctx, id):
    return Issue(ctx.obj.connection, id=id).delete()


@delete.command()
@click.pass_context
@click.argument('id')
def project(ctx, id):
    return Project(ctx.obj.connection, id=id).delete()


@delete.command()
@click.pass_context
@click.argument('login')
def user(ctx, login):
    return User(ctx.obj.connection, login=login).delete()


@delete.command()
@click.pass_context
@click.argument('name')
def group(ctx, name):
    return Group(ctx.obj.connection, name=name).delete()
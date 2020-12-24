# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/quhujun/.pyenv/versions/3.6.0/Python.framework/Versions/3.6/lib/python3.6/site-packages/youtiao/__init__.py
# Compiled at: 2018-05-10 02:33:50
# Size of source mod 2**32: 488 bytes
import click
from youtiao.commands.protoc import protoc
from youtiao.commands.rancher import deploy
from youtiao.commands.docker import build
from youtiao.commands.boilerplate import init_project

@click.group()
def cli():
    """Micro Service Toolkit"""
    pass


cli.add_command(protoc)
cli.add_command(deploy, name='rancher_deploy')
cli.add_command(build, name='build_image')
cli.add_command(init_project, name='init')
if __name__ == '__main__':
    cli()
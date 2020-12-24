# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/cli/admin/install.py
# Compiled at: 2017-04-11 07:05:22
# Size of source mod 2**32: 2386 bytes
"""Installs and configures Treadmill locally."""
import os, click, yaml
from treadmill import context
from treadmill.osmodules import bootstrap
from treadmill import cli

def init():
    """Return top level command handler."""

    @click.group()
    @click.option('--cell', required=True, envvar='TREADMILL_CELL')
    @click.option('--zookeeper', required=True, envvar='TREADMILL_ZOOKEEPER', callback=cli.handle_context_opt)
    @click.option('--config', required=True, type=click.File(), multiple=True)
    @click.pass_context
    def install(ctx, cell, zookeeper, config):
        """Installs Treadmill."""
        if cell == '-':
            cell = None
        if cell:
            context.GLOBAL.cell = cell
            context.GLOBAL.resolve(cell)
        ctx.obj['COMMON_DEFAULTS'] = {}
        for conf in config:
            ctx.obj['COMMON_DEFAULTS'].update(yaml.load(conf.read()))

    @install.command()
    @click.option('--install-dir', default=lambda : os.path.join(bootstrap.default_install_dir(), 'treadmill'))
    @click.option('--run/--no-run', is_flag=True, default=False)
    @click.pass_context
    def node(ctx, install_dir, run):
        """Installs Treadmill node."""
        node_bootstrap = bootstrap.NodeBootstrap(install_dir, ctx.obj['COMMON_DEFAULTS'])
        node_bootstrap.install()
        if run:
            node_bootstrap.run()

    del node
    if os.name != 'nt':

        @install.command()
        @click.option('--install-dir', default=lambda : os.path.join(bootstrap.default_install_dir(), 'treadmill_master'))
        @click.option('--run/--no-run', is_flag=True, default=False)
        @click.option('--master-id', required=True, type=click.Choice(['1', '2', '3']))
        @click.pass_context
        def master(ctx, install_dir, run, master_id):
            """Installs Treadmill master."""
            master_bootstrap = bootstrap.MasterBootstrap(install_dir, ctx.obj['COMMON_DEFAULTS'], master_id)
            master_bootstrap.install()
            if run:
                master_bootstrap.run()

        del master
    return install
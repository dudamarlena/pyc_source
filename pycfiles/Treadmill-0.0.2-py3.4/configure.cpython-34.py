# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/configure.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 748 bytes
"""Treadmill application configuration."""
import logging, click
from treadmill import appmgr
from treadmill.appmgr import configure as app_cfg
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    @click.argument('eventfile', type=click.Path(exists=True))
    def configure(approot, eventfile):
        """Configure local manifest and schedule app to run."""
        app_env = appmgr.AppEnvironment(root=approot)
        container_dir = app_cfg.configure(app_env, eventfile)
        _LOGGER.info('Configured %r', container_dir)

    return configure
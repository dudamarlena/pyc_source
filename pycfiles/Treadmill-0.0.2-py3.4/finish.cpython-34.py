# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/treadmill/sproc/finish.py
# Compiled at: 2017-04-03 02:32:49
# Size of source mod 2**32: 933 bytes
"""Treadmill application finishing."""
import logging, os, click
from .. import appmgr
from .. import context
from .. import logcontext as lc
from ..appmgr import finish as app_finish
_LOGGER = logging.getLogger(__name__)

def init():
    """Top level command handler."""

    @click.command()
    @click.option('--approot', type=click.Path(exists=True), envvar='TREADMILL_APPROOT', required=True)
    @click.argument('container_dir', type=click.Path(exists=True))
    def finish(approot, container_dir):
        """Finish treadmill application on the node."""
        with lc.LogContext(_LOGGER, os.path.basename(container_dir), lc.ContainerAdapter) as (log):
            log.logger.info('finish (approot %s)', approot)
            app_env = appmgr.AppEnvironment(approot)
            app_finish.finish(app_env, context.GLOBAL.zk.conn, container_dir)

    return finish
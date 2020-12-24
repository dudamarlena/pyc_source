# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/up.py
# Compiled at: 2018-08-18 16:12:14
import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    root.run_command('machine:start', internal=True)
    if '--set-hosts' in args:
        root.run_command('hosts:set', internal=True)
        args = filter(lambda s: s != '--set-hosts', args)
    else:
        logger.cmd('Hosts mapping ignored.')
    logger.cmd('Up project <b>%s</b>' % (root.compose.name,))
    cmd = root.bash(root.compose.bin, 'up', compose=root.compose, is_system=True, *args)
    if cmd.is_success:
        logger.success('<b>%s</b> is up.' % (root.compose.name,))
    if root.mounting['hosts']:
        for host in root.mounting['hosts']:
            logger.success('Project is accessible by http://%s.' % (host,))
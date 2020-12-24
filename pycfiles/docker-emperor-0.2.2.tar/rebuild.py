# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/rebuild.py
# Compiled at: 2018-08-18 16:12:30
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    logger.cmd('Rebuild <b>%s</b>' % (root.project.compose.name,))
    root.project.machine.start()
    cmd = root.bash(root.project.compose.bin, '--no-cache', 'build', compose=root.compose, is_system=True, *args)
    if cmd.is_success:
        logger.success('<b>%s</b> rebuilt.' % (root.project.compose.name,))
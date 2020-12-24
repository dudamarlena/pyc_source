# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/build.py
# Compiled at: 2018-08-18 16:12:34
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    logger.cmd('Build <b>%s</b>' % (root.project.compose.name,))
    root.run_command('machine:start', internal=True)
    cmd = root.bash(root.project.compose.bin, 'build', compose=root.compose, is_system=True, *args)
    if cmd.is_success:
        logger.success('<b>%s</b> built.' % (root.project.compose.name,))
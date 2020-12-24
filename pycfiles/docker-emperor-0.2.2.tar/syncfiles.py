# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/syncfiles.py
# Compiled at: 2019-02-03 00:12:04
import os, docker_emperor.logger as logger

def run(root, *args, **kwargs):
    logger.cmd('Sync files for project <b>%s</b>' % (root.compose.name,))
    root.run_command('machine:start', internal=True)
    if not root.mounting.is_localhost:
        for file in root.mounting['files']:
            cmd = root.bash(root.mounting.docker_machine_bin, 'scp', '--quiet', '-r', '-d', file, ('{}:{}').format(root.mounting.docker_machine_name, root.mounting['workdir']), is_system=True)
            print cmd.cmd_line

    else:
        logger.warning(root.mounting.LOCAL_MACHINE_WARNING)
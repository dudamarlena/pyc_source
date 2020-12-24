# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/ssh.py
# Compiled at: 2018-09-05 02:55:25
from docker_emperor.commands import Command
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    mounting = root.mounting
    if mounting.is_localhost:
        logger.warning(mounting.LOCAL_MACHINE_WARNING)
    else:
        cmd = root.bash(mounting.docker_machine_bin, 'ssh', mounting.docker_machine_name, is_system=True, *args)
        if cmd.is_success:
            logger.success('')
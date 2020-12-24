# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/launch.py
# Compiled at: 2018-08-01 09:02:39
import os
from docker_emperor.commands import Command
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    logger.cmd('Run project <b>%s</b>' % (root.compose.name,))
    root.run_command('machine:start', internal=True)
    root.run_command('down', internal=True)
    root.run_command('up', internal=True, *args)
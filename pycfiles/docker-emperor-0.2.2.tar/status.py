# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/status.py
# Compiled at: 2018-07-19 04:04:34
from docker_emperor.commands import Command
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    status = Command(root.machine.bin, 'status', root.machine.name).out
    logger.warning(status)
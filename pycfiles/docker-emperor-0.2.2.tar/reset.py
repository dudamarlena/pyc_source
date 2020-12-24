# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/docker/reset.py
# Compiled at: 2018-08-29 02:03:28
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    logger.cmd('Removing all docker containers..')
    root.bash('docker rm $(docker ps -a -q) -f', compose=root.compose, is_system=True)
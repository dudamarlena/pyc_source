# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/regenerate-certs.py
# Compiled at: 2019-04-11 08:05:17
from docker_emperor.commands import Command
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    Command(root.mounting.docker_machine_bin, 'regenerate-certs', root.mounting.docker_machine_name, is_system=True)
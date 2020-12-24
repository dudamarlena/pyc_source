# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/bash.py
# Compiled at: 2019-05-29 01:58:29
import docker_emperor.logger as logger

def run(root, *args, **kwargs):
    root.bash(compose=root.compose, is_system=True, *args)
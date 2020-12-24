# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dalou/www/DOCKER/docker-emperor/docker_emperor/commands/top.py
# Compiled at: 2018-08-18 16:12:11
import os

def run(root, *args, **kwargs):
    cmd = root.bash(root.project.compose.bin, 'top', compose=root.compose, is_system=True, *args)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/docker-droplet/docker_droplet/down.py
# Compiled at: 2020-02-14 12:43:15
# Size of source mod 2**32: 374 bytes
from os.path import dirname
from subprocess import run

def tear_down(token, config_path) -> None:
    """
    Destroys the terraform infrastructure specified in the config path provided.
    
    Args:
        token ([type]): Digitalocean access token
        config_path ([type]): Terraform config path
    """
    run(['terraform', 'destroy'], cwd=(dirname(config_path)))
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/docker-droplet/docker_droplet/up.py
# Compiled at: 2020-02-14 12:46:21
# Size of source mod 2**32: 1452 bytes
import pathlib
from os import chmod, stat
from os.path import dirname, join
from stat import S_IEXEC
from subprocess import run
import sys
sys.path.append('..')
from docker_droplet.terraform.template import create_config

def set_up(droplet_name, ssh_key, token, project, domain, config_path) -> None:
    """ 
    Call functions to create a terraform configuration and then provision the infrastructure with an ansible playbook.
    
    Args:
        droplet_name ([type]):
        ssh_key ([type]):
        token ([type]):
        project ([type]):
        domain ([type]):
        config_path ([type]):
    """
    with open(config_path, 'w') as (config_file):
        config_text = create_config(droplet_name, ssh_key, project, domain)
        config_file.write(config_text)
    run(['terraform', 'init'], cwd=(dirname(config_path)))
    run(['terraform', 'apply'], cwd=(dirname(config_path)))
    directory = pathlib.Path(__file__).parent.absolute()
    INVENTORY = join(directory, 'ansible/inventory')
    INVENTORY_SCRIPT = join(INVENTORY, 'digitalocean.py')
    PLAYBOOK = join(directory, 'ansible/playbook.yml')
    chmod(INVENTORY_SCRIPT, stat(INVENTORY_SCRIPT).st_mode | S_IEXEC)
    run(['ansible-playbook', '-i', INVENTORY, PLAYBOOK, '-u', 'root'])
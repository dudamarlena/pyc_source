# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/joel/Workspace/docker-droplet/docker_droplet/ansible/inventory/digitalocean.py
# Compiled at: 2020-02-14 12:42:47
# Size of source mod 2**32: 785 bytes
import json
from os import environ
from doboto.DO import DO

def main() -> None:
    """
    Dynamic inventory script for Digitalocean. Targets a single specified droplet. Gets access token and droplet name from environment variables. 
    """
    token = environ.get('TF_VAR_DOCKER_DROPLET_TOKEN')
    name = environ.get('TF_VAR_DOCKER_DROPLET_DROPLET_NAME')
    client = DO(token=token)
    hosts = [d['networks']['v4'][0]['ip_address'] for d in client.droplet.list() if d['name'] == name]
    hosts.reverse()
    print(json.dumps({'_meta':{'hostvars': {}}, 
     'instances':{'hosts':hosts,  'vars':{}}}))


if __name__ == '__main__':
    main()
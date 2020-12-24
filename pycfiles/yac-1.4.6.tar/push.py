# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/x0ox/Dropbox/ActiveDev/yac/yac/lib/container/push.py
# Compiled at: 2017-11-16 20:28:41
from docker import Client
import docker, os, json
from api import get_docker_client

def push_image(image_tag, hub_uname, hub_pwd, hub_email, connection_str='', registry_in='https://index.docker.io/v2'):
    print 'Getting docker client for connection_str=%s' % connection_str
    docker_client = get_docker_client(connection_str)
    docker_client.login(hub_uname, password=hub_pwd, email=hub_email, registry=registry_in)
    for line in docker_client.push(image_tag, stream=True):
        line_json = json.loads(line)
        if 'stream' in line_json:
            print line_json['stream']
        else:
            print line_json
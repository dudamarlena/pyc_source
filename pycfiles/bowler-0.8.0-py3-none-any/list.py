# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/clewis/Desktop/old-air/github-public/bowl/bowl/cli_opts/list.py
# Compiled at: 2014-09-28 15:41:20
__doc__ = '\nThis module is the list command of bowl.\n\nCreated on 14 March 2014\n@author: Charlie Lewis\n'
import ast, docker, os
from bowl.cli_opts import hosts

class Object(object):
    pass


class list(object):
    """
    This class is responsible for the list command of the cli.
    """

    @classmethod
    def main(self, args):
        containers = []
        try:
            directory = args.metadata_path
            directory = os.path.expanduser(directory)
            with open(os.path.join(directory, 'containers'), 'r') as (f):
                for line in f:
                    container = ast.literal_eval(line.rstrip('\n'))
                    containers.append(container['container_id'] + ',' + container['host'])

        except:
            pass

        host_args = Object()
        host_args.metadata_path = args.metadata_path
        host_args.z = True
        host_a = hosts.hosts.main(host_args)
        host_c = []
        for host in host_a:
            c = docker.Client(base_url='tcp://' + host + ':2375', version='1.12', timeout=2)
            host_c.append(c.containers())

        compare_containers = []
        try:
            for container in host_c[0]:
                compare_containers.append(container['Id'])

        except:
            if not args.z:
                print 'no hosts found'
            return ''

        running_containers = []
        for item in containers:
            container_id = item.split(',')[0]
            if container_id in compare_containers:
                running_containers.append(item)

        if not args.z:
            for container in running_containers:
                print container

        return running_containers
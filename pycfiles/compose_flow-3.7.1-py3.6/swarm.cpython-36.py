# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/swarm.py
# Compiled at: 2020-01-28 12:24:29
# Size of source mod 2**32: 2501 bytes
"""
Subcommand for working with the Docker Swarm

The `inspect` action will list all the services running on the swarm

```
compose-flow -e dev swarm inspect
```
"""
import argparse, collections
from compose_flow import docker
from tabulate import tabulate
from .base import BaseSubcommand

def flatten(d, parent_key='', sep='_'):
    items = []
    for k, v in d.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, collections.MutableMapping):
            items.extend(flatten(v, new_key, sep=sep).items())
        else:
            items.append((new_key, v))

    return dict(items)


class Swarm(BaseSubcommand):
    setup_profile = False

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.epilog = __doc__
        subparser.formatter_class = argparse.RawDescriptionHelpFormatter
        subparser.add_argument('action', help='The action to run')

    def action_inspect(self):
        service_status_l = []
        for service in docker.get_services():
            service_name = service['Name']
            service_status = {}
            service_info = {'service':{'name': service_name}, 
             'status':service_status}
            service_config = docker.get_service_config(service_name)
            spec = service_config[0]['Spec']
            task_template = spec['TaskTemplate']
            mode = spec['Mode']
            if 'Global' in mode:
                service_status['has_node_constraint'] = 'Global'
            else:
                placement_constraints = task_template['Placement'].get('Constraints', [])
                service_status['has_node_constraint'] = any([x.startswith('node.role') for x in placement_constraints])
            resources = task_template['Resources']
            service_status['has_limits'] = 'Limits' in resources
            service_status['has_reservations'] = 'Reservations' in resources
            service_status_l.append(service_info)

        flat_l = [flatten(x) for x in service_status_l]
        print(tabulate(flat_l, headers='keys'))
# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/commands/subcommands/service.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 6271 bytes
__doc__ = '\nSubcommand for working with services\n\nThis subcommand provides two actions:\n\n- list\n- exec\n\nThe `list` action will list all the services for a stack when no additional\narguments are given:\n\n```\ncompose-flow -e dev service list\n```\n\nWhen the name of a service is given, the `list` action will list all the\nrunning containers for the specified service:\n\n```\ncompose-flow -e dev service list app\n```\n\nThe `exec` action will execute the given command within the specified container.\nFor example, the following command will launch an interactive shell in the `app`\ncontainer:\n\n```\ncompose-flow -e dev service exec app /bin/bash\n```\n'
import argparse, functools, logging, os, random, shlex, sys, time
from .base import BaseSubcommand
from compose_flow import errors, shell

class Service(BaseSubcommand):
    setup_environment = False
    setup_profile = False

    @classmethod
    def fill_subparser(cls, parser, subparser):
        subparser.epilog = __doc__
        subparser.formatter_class = argparse.RawDescriptionHelpFormatter
        subparser.add_argument('--user',
          '-u', help='the user to become int he container')
        subparser.add_argument('--retries',
          type=int, default=30, help='number of times to retry')
        subparser.add_argument('--ssh',
          action='store_true', help='ssh to the machine, not the container')
        subparser.add_argument('--sudo',
          action='store_true',
          help='use sudo to run the docker command remotely')
        subparser.add_argument('--list',
          action='store_true', help='list available containers')
        subparser.add_argument('--container',
          type=int,
          default=0,
          help='which numbered container to select, default=0')
        subparser.add_argument('--random',
          action='store_true', help='pick a random matching container')
        subparser.add_argument('--service-name',
          help='full service name to use instead of generated')
        subparser.add_argument('action', help='The action to run')
        subparser.add_argument('service', nargs='?', help='The desired service')

    def action_exec(self):
        args = self.workflow.args
        result = None
        for i in range(args.retries):
            try:
                result = self.run_service()
            except errors.NoContainer:
                time.sleep(1.0)
            else:
                break

        if not result:
            sys.exit(f"No container found for service={self.service_name}")

    def action_list(self):
        """
        Lists the stack

        if a service is given, all containers found for the given service are printed
        otherwise all the services in the stack are listed
        """
        service_name = self.service_name
        if service_name:
            print('ALL CONTAINERS:\n')
            for idx, item in enumerate(self.list_containers()):
                print('\t{}: {}'.format(idx, item))

            print(f"\nSELECTED:\n\t{self.select_container()}")
        else:
            print(self.list_services())

    @functools.lru_cache()
    def list_containers(self, service_name: str=None):
        service_name = service_name or self.service_name
        command = f"docker service ps --no-trunc --filter desired-state=running {service_name}"
        proc = self.execute(command)
        items = []
        try:
            output = proc.stdout.decode('utf8').splitlines()[1:]
            output[0]
        except IndexError:
            raise errors.NoContainer()
        else:
            for item in output:
                if f"{service_name}." not in item:
                    pass
                else:
                    items.append(item)

        return items

    def list_services(self):
        """
        Lists all the services for this stack
        """
        proc = self.execute(f"docker stack services {self.workflow.config_name}")
        return proc.stdout.decode('utf8')

    def run_service(self):
        args = self.workflow.args
        line = self.select_container()
        container_info = line.strip()
        container_info_split = container_info.split()
        container_hash = container_info_split[0]
        container_prefix = container_info_split[1]
        container_host = container_info_split[3]
        if container_host.startswith('ip-'):
            container_host = container_host.replace('ip-', '').replace('-', '.')
        host_info = f"{self.workflow.remote.username}@{container_host}"
        docker_user = ''
        if args.user:
            docker_user = f"--user {args.user} "
        else:
            command = f"ssh -t {host_info}"
            docker_command = f"docker exec -t -i {docker_user}{container_prefix}.{container_hash} {' '.join(self.workflow.args_remainder)}"
            if args.sudo:
                docker_command = f"sudo {docker_command}"
            if not args.ssh:
                command = f"{command} {docker_command}"
            else:
                sys.stderr.write(f"docker_command: {docker_command}\n")
        logging.debug(f"command={command}")
        return shell.execute(command, (os.environ), _fg=True)

    def select_container(self):
        args = self.workflow.args
        containers = self.list_containers()
        if args.random:
            return random.choice(containers)
        else:
            return containers[args.container]

    @property
    def service_name(self):
        args = self.workflow.args
        config_name = self.workflow.config_name
        service_name = args.service_name
        if service_name:
            return service_name
        else:
            service_name = args.service
            if not service_name:
                return
            return f"{config_name}_{service_name}"
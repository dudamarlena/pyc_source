# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/environment/backends/swarm_backend.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 3759 bytes
import os, sys, sh
from .base_backend import BaseBackend
from compose_flow import docker
from compose_flow.commands.subcommands.remote import Remote

class SwarmBackend(BaseBackend):
    """SwarmBackend"""

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.remote_cls = kwargs.get('remote_cls', Remote)

    def _check_swarm(self):
        """
        Checks to see if Docker is setup as a swarm
        """
        try:
            self.execute('docker config ls')
        except sh.ErrorReturnCode_1 as exc:
            message = exc.stderr.decode('utf8').strip().lower()
            if 'this node is not a swarm manager' in message:
                self.init_swarm(prompt=True)
            else:
                raise

    def init_swarm(self, prompt: bool=False) -> None:
        """
        Prompts to initialize a local swarm
        """
        try:
            self.execute('docker config ls')
        except:
            pass
        else:
            return
            environment = self.workflow.environment
            docker_host = environment.data.get('DOCKER_HOST')
            if docker_host:
                docker_host_message = f"docker host at {docker_host}"
            else:
                docker_host_message = 'docker host'
            message = f"It looks like your {docker_host_message} is not setup for a swarm.\nSwarm is needed in order to store configuration directly on Docker itself.\n\nWould you like to configure it now? [N|y]: "
            init_swarm = True
            if prompt:
                print(message, end='')
                response = sys.stdin.readline().strip()
                response = response.upper() or 'N'
                if response != 'Y':
                    init_swarm = False
            if init_swarm:
                self.execute('docker swarm init')

    def ls(self) -> list:
        return docker.get_configs()

    def read(self, name: str) -> str:
        config_remote = self.workflow.args.config_remote
        remote = None
        old_docker_host = os.environ.get('DOCKER_HOST')
        try:
            if config_remote:
                print(f"read config from config_remote={config_remote}")
                remote = self.remote_cls(workflow=(self.workflow), name=config_remote)
                remote.connect()
                docker_host = remote.docker_host
                if docker_host:
                    os.environ.update({'DOCKER_HOST': docker_host})
            return docker.get_config(name)
        finally:
            if old_docker_host:
                os.environ.update({'DOCKER_HOST': old_docker_host})
            else:
                os.environ.pop('DOCKER_HOST', None)

    def rm(self, name: str) -> None:
        """
        Removes a config from Swarm
        """
        docker.remove_config(name)

    def write(self, name: str, path) -> None:
        """
        Saves an environment into the swarm
        """
        docker.load_config(name, path)
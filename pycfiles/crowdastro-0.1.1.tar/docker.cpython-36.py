# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /mount/SDC/crowdai/repo2docker/repo2docker/buildpacks/docker.py
# Compiled at: 2018-06-09 10:26:45
# Size of source mod 2**32: 1409 bytes
__doc__ = 'Generates a variety of Dockerfiles based on an input matrix\n'
import os, docker
from .base import BuildPack

class DockerBuildPack(BuildPack):
    """DockerBuildPack"""
    dockerfile = 'Dockerfile'

    def detect(self):
        """Check if current repo should be built with the Docker BuildPack"""
        return os.path.exists(self.binder_path('Dockerfile'))

    def render(self):
        """Render the Dockerfile using by reading it from the source repo"""
        Dockerfile = self.binder_path('Dockerfile')
        with open(Dockerfile) as (f):
            return f.read()

    def build(self, image_spec, memory_limit, build_args):
        """Build a Docker image based on the Dockerfile in the source repo."""
        limits = {'memswap': -1}
        if memory_limit:
            limits['memory'] = memory_limit
        client = (docker.APIClient)(version='auto', **docker.utils.kwargs_from_env())
        for line in client.build(path=(os.getcwd()),
          dockerfile=(self.binder_path(self.dockerfile)),
          tag=image_spec,
          buildargs=build_args,
          decode=True,
          forcerm=True,
          rm=True,
          container_limits=limits):
            yield line
# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/jfischer/code/repo2docker/repo2docker/buildpacks/docker.py
# Compiled at: 2019-09-18 03:20:22
# Size of source mod 2**32: 2003 bytes
"""Generates a variety of Dockerfiles based on an input matrix
"""
import os, docker
from .base import BuildPack

class DockerBuildPack(BuildPack):
    __doc__ = 'Docker BuildPack'
    dockerfile = 'Dockerfile'

    def detect(self):
        """Check if current repo should be built with the Docker BuildPack"""
        return os.path.exists(self.binder_path('Dockerfile'))

    def render(self):
        """Render the Dockerfile using by reading it from the source repo"""
        Dockerfile = self.binder_path('Dockerfile')
        with open(Dockerfile) as (f):
            return f.read()

    def build(self, client, image_spec, memory_limit, build_args, cache_from, extra_build_kwargs):
        """Build a Docker image based on the Dockerfile in the source repo."""
        if not isinstance(memory_limit, int):
            raise ValueError("The memory limit has to be specified as aninteger but is '{}'".format(type(memory_limit)))
        limits = {}
        if memory_limit:
            limits = {'memory':memory_limit, 
             'memswap':memory_limit}
        build_kwargs = dict(path=(os.getcwd()),
          dockerfile=(self.binder_path(self.dockerfile)),
          tag=image_spec,
          buildargs=build_args,
          decode=True,
          forcerm=True,
          rm=True,
          container_limits=limits,
          cache_from=cache_from)
        build_kwargs.update(extra_build_kwargs)
        for line in (client.build)(**build_kwargs):
            yield line
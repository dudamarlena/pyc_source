# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/environment/backends/base_backend.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 1078 bytes
import logging
from compose_flow.errors import BackendError

class BaseBackend(object):

    def __init__(self, *args, **kwargs):
        workflow = kwargs.get('workflow')
        if workflow:
            self.workflow = workflow
        else:
            raise BackendError('must pass workflow')

    @property
    def logger(self):
        return logging.getLogger(f"{__name__}.{self.__class__.__name__}")

    def ls(self):
        """List the available environments"""
        raise NotImplementedError()

    def read(self, name: str):
        """Read a specific environment"""
        raise NotImplementedError()

    def rm(self, name: str):
        """
        Removes an environment from the backend

        Args:
            name: name of the environment to remove
        """
        raise NotImplementedError()

    def write(self, name: str, path: str):
        """
        Writes the environment to the backend

        Args:
            name: the environment name
            path: the path to the config on disk
        """
        raise NotImplementedError()
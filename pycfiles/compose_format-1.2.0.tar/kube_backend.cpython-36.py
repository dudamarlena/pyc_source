# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/environment/backends/kube_backend.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 1227 bytes
import os
from .base_backend import BaseBackend
from compose_flow.kube.mixins import KubeMixIn
from compose_flow import shell

class KubeBackend(BaseBackend, KubeMixIn):
    """KubeBackend"""
    kubectl_command = 'kubectl'
    env_key = '_env'

    def __init__(self, *args, **kwargs):
        (super().__init__)(*args, **kwargs)
        self.secret_exists = None
        self.workflow = kwargs.get('workflow')
        self.switch_kube_context()
        self._check_kube_context()
        self._check_kube_namespace()

    @property
    def namespace(self):
        return f"compose-flow-{self.workflow.args.profile}"

    def execute(self, command: str, **kwargs):
        env = os.environ
        return (shell.execute)(command, env, **kwargs)

    def ls(self) -> list:
        """List kubectl secrets in the proper namespace"""
        return self._list_secrets()

    def read(self, name: str) -> str:
        return self._read_secret_env(name)

    def rm(self, name: str) -> None:
        self._remove_secret(name)

    def write(self, name: str, path) -> None:
        """
        Saves an environment into a Secret
        """
        return self._write_secret_env(name, path)
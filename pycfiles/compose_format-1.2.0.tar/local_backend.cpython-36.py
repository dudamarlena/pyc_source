# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/compose_flow/environment/backends/local_backend.py
# Compiled at: 2020-05-06 10:05:57
# Size of source mod 2**32: 1467 bytes
import os
from compose_flow.settings import APP_ENVIRONMENTS_ROOT
from .base_backend import BaseBackend

class LocalBackend(BaseBackend):
    """LocalBackend"""

    def __init__(self, *args, root=None, **kwargs):
        """
        Constructor

        Args:
            root: the base directory where to look for local environment files
        """
        (super().__init__)(*args, **kwargs)
        self.root = root or APP_ENVIRONMENTS_ROOT

    def ls(self):
        if not os.path.exists(self.root):
            return []
        else:
            return os.listdir(self.root)

    def get_path(self, name: str) -> str:
        return os.path.join(self.root, name)

    def read(self, name: str) -> str:
        """
        Reads in the environment file
        """
        path = self.get_path(name)
        if not os.path.exists(path):
            return ''
        with open(path, 'r') as (fh):
            return fh.read()

    def rm(self, name: str) -> None:
        """
        Removes an environment file
        """
        path = self.get_path(name)
        if os.path.exists(path):
            os.remove(path)

    def write(self, name: str, path: str) -> None:
        if not os.path.exists(self.root):
            os.makedirs(self.root)
        with open(path, 'r') as (fh):
            buf = fh.read()
        with open(self.get_path(name), 'w') as (fh):
            fh.write(buf)
# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.munaro/workspace/brokerpackager/brokerpackager/managers/python.py
# Compiled at: 2017-08-18 13:56:37
# Size of source mod 2**32: 1067 bytes
import subprocess
from .base import BaseManager

class PyManager(BaseManager):

    def do_install(self, package, pip_paths, *args):
        (self.log_install)(package, *pip_paths, *args)
        for pip_path in pip_paths:
            subprocess.call([pip_path, 'install', package, *args])

    def install(self, package, version, git, pip_paths=['pip']):
        if package:
            if git:
                self.do_install('git+{}'.format(package), pip_paths)
            else:
                if version:
                    self.do_install('{}=={}'.format(package, version), pip_paths)
                else:
                    self.do_install('{}'.format(package), pip_paths, '-U')

    def install_list(self, package_list, extra_config={}):
        pip_paths = extra_config.get('pip_paths', ['pip'])
        for package_item in package_list:
            package = package_item.get('name')
            version = package_item.get('version')
            git = package_item.get('git')
            self.install(package, version, git, pip_paths)
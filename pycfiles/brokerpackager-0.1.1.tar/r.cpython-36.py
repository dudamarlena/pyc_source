# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/diogo.munaro/workspace/brokerpackager/brokerpackager/managers/r.py
# Compiled at: 2017-08-16 14:26:03
# Size of source mod 2**32: 1142 bytes
import rpy2.robjects.packages as rpackages
from .base import BaseManager

class RManager(BaseManager):

    def __init__(self, log_file=''):
        super(RManager, self).__init__(log_file)
        self.devtools = rpackages.importr('devtools')
        self.utils = rpackages.importr('utils')

    def install_version(self, package, version):
        self.devtools.install_version(package, version=version)

    def install(self, package, version, git):
        self.log_install(package, version, git)
        if package:
            if git:
                self.install_git(package)
            else:
                if version:
                    self.install_version(package, version)
                else:
                    self.utils.install_packages(package)

    def install_git(self, repo):
        self.devtools.install_git(repo)

    def install_list(self, package_list, extra_config={}):
        for package_item in package_list:
            package = package_item.get('name')
            version = package_item.get('version')
            git = package_item.get('git')
            self.install(package, version, git)
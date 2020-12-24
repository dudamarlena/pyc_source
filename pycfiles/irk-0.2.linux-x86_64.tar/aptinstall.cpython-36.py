# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/installers/aptinstall.py
# Compiled at: 2018-06-20 20:07:32
# Size of source mod 2**32: 1316 bytes
from .common import Installer, InstallerState
from ..util import proc

class AptInstaller(Installer):

    def __init__(self, package, exec):
        self.package = package
        self.exec = exec

    def install(self, dry_run):
        args = [
         self.exec, 'install', self.package, '-y']
        if dry_run:
            print(f"Would run {' '.join(args)}")
            return InstallerState.OK
        code, stdout = proc.run(args)
        if code == 0:
            return InstallerState.OK
        if 'are you root?' in stdout:
            return InstallerState.NEEDS_SUDO
        else:
            if 'E: Unable to locate package' in stdout:
                return InstallerState.INVALID_NAME
            return InstallerState.FAILED

    def remove(self, dry_run):
        args = [self.exec, 'remove', self.package, '-y']
        if dry_run:
            print(f"Would run {' '.join(args)}")
            return InstallerState.OK
        code, stdout = proc.run(args)
        if code == 0:
            return InstallerState.OK
        if 'are you root?' in stdout:
            return InstallerState.NEEDS_SUDO
        else:
            if 'E: Unable to locate package' in stdout:
                return InstallerState.INVALID_NAME
            return InstallerState.FAILED

    def get_dependencies(self):
        return []
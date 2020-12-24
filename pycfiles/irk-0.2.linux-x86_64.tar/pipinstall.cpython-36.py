# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python3.6/dist-packages/irk/installers/pipinstall.py
# Compiled at: 2018-06-20 20:14:45
# Size of source mod 2**32: 1468 bytes
from .common import InstallerState, Installer
from ..util import proc

class PipInstaller(Installer):

    def __init__(self, package_name, version):
        self.executable = 'pip' + (version if version is not None else '')
        self.package = package_name

    def install(self, dry_run):
        arg_string = [
         '/usr/bin/env', self.executable, 'install', self.package]
        if dry_run:
            print('Would run {}'.format(' '.join(arg_string)))
            return InstallerState.OK
        print(f"Running {' '.join(arg_string)}")
        code, stdout = proc.run(arg_string)
        if code == 0:
            return InstallerState.OK
        if '[Errno 13]' in stdout:
            return InstallerState.NEEDS_SUDO
        else:
            if 'No matching distribution' in stdout:
                return InstallerState.INVALID_NAME
            return InstallerState.FAILED

    def remove(self, dry_run):
        arg_string = [
         '/usr/bin/env', self.executable, 'uninstall', self.package, '-y']
        if dry_run:
            print('Would run {}'.format(' '.join(arg_string)))
            return InstallerState.OK
        print(f"Running {' '.join(arg_string)}")
        code, stdout = proc.run(arg_string)
        if 'as it is not installed' in stdout:
            return InstallerState.INVALID_NAME
        else:
            if code == 0:
                return InstallerState.OK
            return InstallerState.FAILED